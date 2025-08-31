import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

client = OpenAI()
MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

def classify_with_openai(text: str) -> Dict[str, Any]:
    """
    Classifies the text using the OpenAI API, requesting a structured JSON output.
    """
    if not client.api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    if not text.strip():
        return {"category": "N/A", "confidence": 0.0}

    prompt = f"""
    Analyze the following email and classify it as 'Produtivo' or 'Improdutivo'.
    - 'Produtivo' refers to work emails, tasks, reports, etc.
    - 'Improdutivo' refers to personal emails, socialization, spam, etc.

    Also provide a confidence level for your decision, from 0.0 to 1.0.

    Respond ONLY with a JSON object containing the keys "category" and "confidence".

    Email to analyze:
    ---
    "{text}"
    ---
    """

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0,
            response_format={"type": "json_object"},
        )

        result = json.loads(resp.choices[0].message.content)
        
        if "category" in result and "confidence" in result:
            return result
        else:
            return {"category": "Formatting Error", "confidence": 0.0}

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return {"category": "API Error", "confidence": 0.0}


def generate_response_openai(text: str, category: str) -> str:
    """
    Generates an email response based on the text and category.
    """
    if not client.api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    
    if category == "Produtivo":
        instruction = "Generate a short, professional, and positive response to the email."
    else:
        instruction = "Generate a short, polite, and neutral response to the email, indicating that the message has been received."

    template = (
        f"The received email is:\n\n\"\"\"{text}\"\"\"\n\n"
        f"The category was: {category}.\n\n"
        f"Instruction: {instruction}\n\n"
        "Suggested response:"
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": template}],
        max_tokens=100,
        temperature=0.5
    )
    return resp.choices[0].message.content.strip()