
from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

APP_NAME = "ɹɐʇsᴉɐꓤ AI"

SYSTEM_PROMPT = """
You are ɹɐʇsᴉɐꓤ AI, a friendly and intelligent AI assistant.

LANGUAGE RULES:
- If the user writes Hindi using English letters,
  reply in Roman Hinglish.
- Never use Devanagari Hindi when the user
  writes in Roman Hinglish.
- Example: Write "Tum kaise ho?"
  not "तुम कैसे हो?"
- If the user writes English, reply in English.
- If the user writes Hindi in Devanagari,
  reply in Devanagari Hindi.

CONVERSATION STYLE:
- Talk naturally and warmly.
- Be friendly, helpful and respectful.
- Understand the user's question before answering.
- Keep simple answers short.
- Explain difficult topics clearly.
- Give examples when useful.
- Ask questions when clarification is needed.
- Avoid robotic and repetitive replies.
- Never invent facts.
- Admit when you are unsure.

You can help with:
General Knowledge, Anime, Gaming,
Technology, Programming and Education.

Remember the context of the current conversation.
"""

@app.route("/")
def home():
    return APP_NAME + " SERVER ONLINE"


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "reply": "Apna message likho."
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
                    "content": SYSTEM_PROMPT
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
