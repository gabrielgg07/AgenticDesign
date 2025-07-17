import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from huggingface_hub import HfFolder


import torch
print("GPU available:", torch.cuda.is_available())
print("Current device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model device:", model.device)




# === ENV SETUP ===
load_dotenv()  # Load from .env if available
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "") 

# === CONFIG ===
DOCUMENTS_FOLDER = "./financeBuddy/financeDocs/"
SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".md"]
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
FAISS_PATH = "faiss_index"

# === LOAD DOCUMENTS ===
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
all_docs = []

print(f"📂 Loading documents from: {DOCUMENTS_FOLDER}")
for filename in os.listdir(DOCUMENTS_FOLDER):
    ext = os.path.splitext(filename)[-1].lower()
    path = os.path.join(DOCUMENTS_FOLDER, filename)

    try:
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        elif ext == ".md":
            loader = UnstructuredMarkdownLoader(path)
        else:
            print(f"⚠️ Skipping unsupported file: {filename}")
            continue

        docs = loader.load()
        chunks = text_splitter.split_documents(docs)
        all_docs.extend(chunks)
        print(f"✅ {filename}: {len(chunks)} chunks")

    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")

print(f"📄 Total chunks loaded: {len(all_docs)}")

# === CLEAN AND PREP TEXT ===
texts = [doc.page_content.strip() for doc in all_docs if doc.page_content.strip()]

if not texts:
    raise ValueError("❌ No valid document content found after preprocessing.")

# === EMBEDDING ===
print(f"🔗 Initializing Mistral embeddings...")
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # 👈 force CPU here
)



print(f"🧠 Embedding {len(texts)} text chunks. This may take a minute...")
vectorstore = FAISS.from_texts(texts, embedding)
vectorstore.save_local(FAISS_PATH)

print(f"✅ Done! Embeddings saved to: {FAISS_PATH}")
