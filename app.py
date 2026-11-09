from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

APP_NAME = "ɹɐʇsᴉɐꓤ AI"

@app.route("/")
def home():
    return APP_NAME + " GROQ SERVER ONLINE"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "reply": "Please type a message."
            }), 400

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            return jsonify({
                "reply": "GROQ_API_KEY setup pending hai."
            }), 503

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are ɹɐʇsᴉɐꓤ AI. "
                        "Reply in the same language and script as the user. "
                        "If the user writes Hinglish in Roman letters, "
                        "reply in Hinglish using Roman letters. "
                        "If the user writes English, reply in English. "
                        "If the user writes Hindi, reply in Hindi. "
                        "Keep every answer short and simple. "
                        "Use 3 to 5 sentences for normal questions. "
                        "Use bullet points when needed. "
                        "Do not give long explanations unless asked. "
                        "Avoid unnecessary tables and Markdown. "
                        "Give accurate answers and admit uncertainty."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception:
        app.logger.exception("Groq chat error")

        return jsonify({
            "reply": "Server error. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
