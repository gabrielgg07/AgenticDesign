import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from fastmcp import FastMCP
from typing import Annotated, Dict
from pydantic import Field

lang_mcp = FastMCP(
    name="langChain MCP server", instructions="Your task is to provide context returned from the embedded financial documents"
)

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # 👈 force CPU here
)
# === Load the FAISS vectorstore ===
DB_PATH = "faiss_index"  # wherever you saved it
vectorstore = FAISS.load_local(DB_PATH, embedding, allow_dangerous_deserialization=True)


# === Create a retriever from the vectorstore ===
retriever = vectorstore.as_retriever(search_type="similarity", k=3)


@lang_mcp.tool(
    name="query_documents",
    description="Fetches all relevant chunks from the documents by matching the query to the docs semantically"
) 
def query_documents(
    query: Annotated[str, Field(description="A search string to query the document database semantically.")]
) -> Dict[str, str]:
    docs = retriever.get_relevant_documents(query)
    results: Dict[str, str] = {}

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        content = doc.page_content.strip()

        if source in results:
            results[source] += "\n\n" + content
        else:
            results[source] = content

    return results