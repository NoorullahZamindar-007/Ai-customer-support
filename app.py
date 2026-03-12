from flask import Flask, jsonify, render_template, request

from config import Config
from database import Database
from services.hf_service import HuggingFaceService


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    database = Database(app.config["DATABASE_PATH"])
    database.init_db()

    hf_service = HuggingFaceService(
        api_token=app.config["HF_API_TOKEN"],
        model_name=app.config["HF_MODEL_NAME"],
        timeout=app.config["HF_API_TIMEOUT"],
        system_prompt=app.config["SYSTEM_PROMPT"],
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health_check():
        return jsonify(
            {
                "status": "ok",
                "service": "ai-customer-support-chatbot",
                "model": app.config["HF_MODEL_NAME"],
            }
        )

    @app.get("/api/logs")
    def get_logs():
        logs = database.fetch_recent_logs(limit=app.config["LOGS_LIMIT"])
        return jsonify({"logs": logs})

    @app.post("/api/chat")
    def chat():
        if not request.is_json:
            return jsonify({"error": "Request must be JSON."}), 400

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Invalid JSON payload."}), 400

        message = payload.get("message", "")
        if not isinstance(message, str):
            return jsonify({"error": "The message must be a string."}), 400

        cleaned_message = message.strip()
        if not cleaned_message:
            return jsonify({"error": "Message cannot be empty."}), 400

        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address and "," in ip_address:
            ip_address = ip_address.split(",")[0].strip()

        try:
            reply = hf_service.generate_reply(cleaned_message)
            log_id = database.save_chat_log(
                user_message=cleaned_message,
                bot_reply=reply,
                status="success",
                ip_address=ip_address,
            )
            return jsonify({"reply": reply, "status": "success", "log_id": log_id}), 200
        except RuntimeError as exc:
            log_id = database.save_chat_log(
                user_message=cleaned_message,
                bot_reply=None,
                status="error",
                error_message=str(exc),
                ip_address=ip_address,
            )
            return (
                jsonify(
                    {
                        "error": str(exc),
                        "status": "error",
                        "log_id": log_id,
                    }
                ),
                502,
            )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
