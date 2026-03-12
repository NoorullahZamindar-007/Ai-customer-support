import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATABASE_PATH = os.path.join(MODELS_DIR, "chat_logs.db")

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
    HF_API_TIMEOUT = int(os.getenv("HF_API_TIMEOUT", "30"))
    HF_API_BASE_URL = os.getenv(
        "HF_API_BASE_URL",
        "https://router.huggingface.co/v1",
    )
    LOGS_LIMIT = int(os.getenv("LOGS_LIMIT", "20"))
    DATABASE_PATH = DATABASE_PATH
    SYSTEM_PROMPT = (
        "You are a professional customer support assistant for a business website. "
        "Be polite, concise, and helpful. Keep answers short and easy to read. "
        "Do not invent company-specific policies, prices, delivery promises, or refund rules. "
        "If the answer depends on company policy or you are unsure, say that the request should be "
        "forwarded to human support. Support common topics like pricing, refunds, delivery, contact, "
        "working hours, and services. If the user asks for harmful, illegal, or irrelevant content, "
        "respond safely and redirect them back to support-related questions."
    )
