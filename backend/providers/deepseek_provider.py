import os
import requests

class DeepSeekProvider:
    def chat(self, messages):
        try:
            r = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"},
                json={"model": "deepseek-chat", "messages": messages}
            )
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            return None