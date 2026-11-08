from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "ɹɐʇsᴉɐꓤ AI V34 - AI SERVER ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        message = (request.get_json(silent=True) or {}).get(
            "message", ""
        ).strip()

        if not message:
            return jsonify({"reply": "Please type a message."}), 400

        if len(message) > 10000:
            return jsonify({"reply": "Message is too long."}), 400

        api_key = os.environ.get("OPENAI_API_KEY")

        if not api_key:
            return jsonify({
                "reply": "AI setup pending. Ask your administrator."
            }), 503

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-5.5"),
            instructions=(
                "You are ɹɐʇsᴉɐꓤ AI. "
                "You are a helpful assistant. "
                "Reply in Hindi or Hinglish when the user does. "
                "Help with general knowledge, anime, Naruto, "
                "Tokyo Revengers, gaming and technology. "
                "Give accurate answers and admit uncertainty."
            ),
            input=message
        )

        return jsonify({"reply": response.output_text})

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "reply": "AI server error. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
      
