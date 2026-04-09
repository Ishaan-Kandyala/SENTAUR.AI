import os
from openai import OpenAI

class MistralProvider:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            print("⚠️ MistralProvider: No MISTRAL_API_KEY found. Skipping Mistral.")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.mistral.ai/v1"
            )

    def chat(self, messages):
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model="mistral-large-latest",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ MistralProvider skipped: {e}")
            return None
