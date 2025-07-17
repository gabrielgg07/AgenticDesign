from google.adk.models.lite_llm import LiteLlm
import litellm

class Llama3Client(LiteLlm):
    def __init__(self):
        model_id = "ollama/deepseek-coder"

        model_list = [
            {
                "model_name": model_id,
                "litellm_provider": "ollama",
                "api_base": "http://localhost:11434",
                "model_info": {"mode": "chat"},
            }
        ]

        super().__init__(
            model=model_id,  # 🔥 FULL ID REQUIRED
            litellm_provider="ollama",
            api_base="http://localhost:11434",
            max_tokens=2048,
            litellm_settings={"model_list": model_list},
        )

        litellm.model_list = model_list
        self.llm_client = litellm
