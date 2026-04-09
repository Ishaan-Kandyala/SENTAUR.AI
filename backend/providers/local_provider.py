from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalProvider:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    def chat(self, messages):
        text = messages[-1]["content"]
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)