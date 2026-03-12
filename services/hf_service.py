import os
from typing import Dict, List

import requests
from dotenv import load_dotenv


load_dotenv()


class HuggingFaceService:
    def __init__(self, api_token: str, model_name: str, timeout: int, system_prompt: str) -> None:
        self.api_token = api_token
        self.model_name = model_name
        self.timeout = timeout
        self.system_prompt = system_prompt
        base_url = os.getenv("HF_API_BASE_URL", "https://router.huggingface.co/v1").rstrip("/")
        self.api_url = f"{base_url}/chat/completions"

    def _build_messages(self, user_message: str) -> List[Dict[str, str]]:
        # The chat-completions API expects a list of role-based messages.
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message.strip()},
        ]

    def generate_reply(self, user_message: str) -> str:
        if not self.api_token:
            raise RuntimeError("Hugging Face API token is missing.")

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, object] = {
            "model": self.model_name,
            "messages": self._build_messages(user_message),
            "max_tokens": 180,
            "temperature": 0.3,
        }

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
        except requests.Timeout as exc:
            raise RuntimeError("The AI service timed out. Please try again.") from exc
        except requests.RequestException as exc:
            raise RuntimeError("Could not connect to the AI service.") from exc

        if response.status_code >= 400:
            error_details = self._extract_error(response)
            raise RuntimeError(f"Hugging Face API error: {error_details}")

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError("The AI service returned invalid JSON.") from exc

        reply = self._parse_reply(data)
        if not reply:
            raise RuntimeError("The AI service returned an empty response.")

        return reply.strip()

    def _extract_error(self, response: requests.Response) -> str:
        try:
            data = response.json()
        except ValueError:
            return response.text.strip() or f"HTTP {response.status_code}"

        if isinstance(data, dict):
            if data.get("error"):
                return str(data["error"])
            if data.get("message"):
                return str(data["message"])

        return str(data)

    def _parse_reply(self, data: object) -> str:
        if not isinstance(data, dict):
            return ""

        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            return ""

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            return ""

        message = first_choice.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            return message["content"]

        delta = first_choice.get("delta")
        if isinstance(delta, dict) and isinstance(delta.get("content"), str):
            return delta["content"]

        return ""
