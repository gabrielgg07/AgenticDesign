# llm_agents/adk_client.py

import os, uuid
from dotenv import load_dotenv
from datetime import datetime
import httpx
import litellm
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

class OpenAIClient(LiteLlm):
    def __init__(self, model_name="openai/gpt-3.5-turbo", **kwargs):
        litellm.aclient_session = httpx.AsyncClient(verify=False)

        

        model = model_name

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

        print(f"[OpenAIClient] Model: {model_name}")
        print(f"[OpenAIClient] API Key Starts With: {api_key[:5]}...")

        requiest_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "x-request-id": str(uuid.uuid4()),
            "x-correlation-id": str(uuid.uuid4()),
            "x-request-date": datetime.utcnow().isoformat(),
        }
        

        super().__init__(model=model_name, api_base=base_url,extra_headers=requiest_headers, max_tokens=2000,**kwargs)