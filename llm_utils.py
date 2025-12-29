from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(text: str) -> str:
    if not text.strip():
        return "No readable text found in screenshot."

    prompt = f"""
    You are analyzing text extracted from a screenshot.

    Your task:
    - Produce a precise, content-faithful summary
    - Preserve key distinctions and examples
    - Do NOT oversimplify
    - Do NOT add information that is not present

    Guidelines:
    - 3–4 sentences maximum
    - Capture contrasts (e.g., books vs periodicals)
    - Mention social implications if present

    Text:
    {text}
    """


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
