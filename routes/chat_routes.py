# routes/chat_routes.py

from flask import Blueprint, request, jsonify
from faiss_chat import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    result = get_chat_response(user_input)  # 수정
    return jsonify(result)  # 그대로 반환 (response + sources)