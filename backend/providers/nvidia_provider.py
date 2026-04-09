import os
from openai import OpenAI

class NvidiaProvider:
    def __init__(self):
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            print("⚠️ NvidiaProvider: No NVIDIA_API_KEY found. Skipping Nvidia.")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://integrate.api.nvidia.com/v1"
            )

    def chat(self, messages):
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ NvidiaProvider skipped: {e}")
            return None
