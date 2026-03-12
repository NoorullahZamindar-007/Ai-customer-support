# AI Customer Support Chatbot

A complete Flask web application that provides a customer support chatbot UI, sends questions to a Hugging Face model, and stores chat logs in SQLite.

## Features

- Clean web chat interface with user and bot chat bubbles
- Flask backend with REST API endpoints
- Hugging Face Inference API integration
- SQLite logging for every chat request
- JSON validation and proper HTTP status codes
- Loading state and frontend error handling
- Environment-based configuration with `python-dotenv`
- Beginner-friendly project structure

## Project Structure

```text
project/
|-- app.py
|-- config.py
|-- database.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- services/
|   |-- __init__.py
|   `-- hf_service.py
|-- templates/
|   `-- index.html
|-- static/
|   |-- style.css
|   `-- script.js
`-- models/
    `-- chat_logs.db
```

## Requirements

- Python 3.10+
- A Hugging Face account and API token

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.

```powershell
Copy-Item .env.example .env
```

4. Update `.env` with your values.

```env
SECRET_KEY=change-me
HF_API_TOKEN=your_hugging_face_api_token
HF_MODEL_NAME=google/flan-t5-large
HF_API_TIMEOUT=30
LOGS_LIMIT=20
```

## Run the App

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## API Endpoints

### `GET /`
Renders the chatbot web interface.

### `GET /api/health`
Returns a health response.

Example response:

```json
{
  "status": "ok",
  "service": "ai-customer-support-chatbot",
  "model": "google/flan-t5-large"
}
```

### `POST /api/chat`
Sends a user message to the chatbot and returns the AI response.

Request body:

```json
{
  "message": "What are your working hours?"
}
```

Success response:

```json
{
  "reply": "Our working hours may vary by team. Please contact support for exact availability.",
  "status": "success",
  "log_id": 1
}
```

Error response:

```json
{
  "error": "Hugging Face API error: ...",
  "status": "error",
  "log_id": 2
}
```

### `GET /api/logs`
Returns recent chat logs for development use.

## Example cURL Request

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Can I get help with a refund?"}'
```

## Example Test Questions

- `What services do you offer?`
- `What are your working hours?`
- `How can I contact support?`
- `Can I request a refund?`
- `How long does delivery take?`
- `Do you have pricing information?`
- `I need help with my order status.`

## Logging Details

The application stores chat requests in `models/chat_logs.db` with these fields:

- `id`
- `user_message`
- `bot_reply`
- `created_at`
- `status`
- `error_message`
- `ip_address`

## Notes

- The Hugging Face token is loaded from `.env` and is never hardcoded.
- Empty or whitespace-only messages are rejected.
- If the AI is unsure or unavailable, the app returns a safe support-oriented response path.
- The default model in this project is `google/flan-t5-large`, but you can switch to any compatible text generation model in `.env`.
