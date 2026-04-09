import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "models/gemini-2.5-flash"

    def chat(self, messages):
        try:
            # Combine all messages into a single prompt
            prompt = ""
            for m in messages:
                role = m["role"]
                content = m["content"]
                if role == "system":
                    prompt += f"System: {content}\n"
                elif role == "user":
                    prompt += f"User: {content}\n"
                elif role == "assistant":
                    prompt += f"Assistant: {content}\n"

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return response.text

        except Exception as e:
            print("Gemini failed:", e)
            return None