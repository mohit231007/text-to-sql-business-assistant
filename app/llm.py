from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings


def get_llm() -> ChatGoogleGenerativeAI:
    settings = get_settings()
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing. Add it to your .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=settings.google_api_key,
    )
