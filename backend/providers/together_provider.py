import os
from openai import OpenAI

class TogetherProvider:
    def __init__(self):
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            print("⚠️ TogetherProvider: No TOGETHER_API_KEY found. Skipping Together AI.")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.together.xyz/v1"
            )

    def chat(self, messages):
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ TogetherProvider skipped: {e}")
            return None
