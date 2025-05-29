# routes/chat_routes.py

from flask import Blueprint, request, jsonify
from faiss_chat import get_chat_response

chat_bp = Blueprint("chat", __name__)

# @chat_bp.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message", "")
#     result = get_chat_response(user_input)  # 수정
#     return jsonify(result)  # 그대로 반환 (response + sources)

# 디버깅용 코드
from flask import Blueprint, request, jsonify
from faiss_chat import get_chat_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    # 🔍 요청 들어온 질문 확인
    print("📩 사용자 질문:", user_input)
    
    result = get_chat_response(user_input)
    
    # 🔍 LLM 또는 FAISS에서 받은 결과 확인
    print("🧠 LLM 응답 전체:", result)
    print("📝 답변 내용:", result.get("response"))
    print("📎 문서 링크:", result.get("sources"))

    return jsonify(result)