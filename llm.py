import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()


# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def create_chat_completion(prompt):
    chat_completion = client.chat.completions.create(
        model="gpt-4-1106-preview", messages=[{"role": "system", "content": prompt}]
    )
    return chat_completion.choices[0].message.content.strip()
