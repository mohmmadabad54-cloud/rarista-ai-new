
from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "ɹɐʇsᴉɐꓤ AI GROQ SERVER ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"reply": "Apna message likho."}), 400

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
                        "Reply in the same language and script used by the user. "
"Use Hinglish in Roman letters when the user writes Hinglish. "
"Use English when the user writes English. "
"Use Hindi when the user writes Hindi. "
                        "Help with general knowledge, anime, "
                        "gaming and technology. "
                        "Be accurate and admit uncertainty."
                    )
                },
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Groq chat error")
        return jsonify({
            "reply": "Groq server error. Render Logs check karo."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
        )
    
