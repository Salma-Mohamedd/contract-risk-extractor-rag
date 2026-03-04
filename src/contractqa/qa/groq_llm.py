from groq import Groq
from contractqa.config import settings

client = Groq(api_key=settings.groq_api_key)

def groq_chat(messages: list[dict]) -> str:
    """
    messages = [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    resp = client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=settings.temperature,
    )
    return resp.choices[0].message.content
