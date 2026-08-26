from app.core import settings
from openai import OpenAI



class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key = settings.OPENROUTER_API_KEY or "dummy-key-for-testing",
            base_url = settings.OPENROUTER_BASE_URL
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model = settings.MODEL_NAME,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        return response.choices[0].message.content
        


llm_client = LLMClient()

