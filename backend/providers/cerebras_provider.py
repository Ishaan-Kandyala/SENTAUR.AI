import os
from openai import OpenAI

class CerebrasProvider:
    def __init__(self):
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            print("⚠️ CerebrasProvider: No CEREBRAS_API_KEY found. Skipping Cerebras.")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.cerebras.ai/v1"
            )

    def chat(self, messages):
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ CerebrasProvider skipped: {e}")
            return None
