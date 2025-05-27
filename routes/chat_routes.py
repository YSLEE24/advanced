# routes/chat_routes.py

from flask import Blueprint, request, jsonify
from chatbot.qa_chain import get_answer

chat_bp = Blueprint("chat", __name__)  # ✅ 이름을 chat_bp로

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    answer = get_answer(user_input)
    return jsonify({"answer": answer})
