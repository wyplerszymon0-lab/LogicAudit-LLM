import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMBridge:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def get_llm_calculation(self, prompt: str, csv_content: str) -> float:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a precise financial auditor. Return only the final number (float)."},
                {"role": "user", "content": f"Data:\n{csv_content}\n\nTask: {prompt}"}
            ]
        )
        try:
            return float(response.choices[0].message.content.strip())
        except ValueError:
            return 0.0
