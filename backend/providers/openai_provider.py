import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("⚠️ OpenAIProvider: No OPENAI_API_KEY found. Skipping OpenAI.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages):
        # If no key or client, skip immediately
        if not self.client:
            return None

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ OpenAIProvider skipped: {e}")
            return None