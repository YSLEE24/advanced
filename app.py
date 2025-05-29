from flask import Flask, request, jsonify
from faiss_chat import get_chat_response
from routes import register_routes

# /chat 라우트 함수 정의
def register_chat_route(app):
    @app.route("/chat", methods=["POST"])
    def chat():
        try:
            # 받은 질문을 json에서 꺼내기
            user_input = request.json.get("message", "")

            # ✅ 문자열만 전달하도록 수정
            result = get_chat_response(user_input)

            # 응답을 json 형식으로 반환 -> 응답이 반드시 JSON 형식이어야 response.response 같은 식으로 접근 가능
            return jsonify({
                "response": result["response"],
                "sources": result.get("sources", [])  # 출처 표시
            })
        except Exception as e:
            # 오류 발생 시 예외 메시지를 json으로
            return jsonify({"error": str(e)}), 500

# 초기 실행 -> Flask 앱 생성
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testsecretkey'

    register_routes(app)           # 기존 페이지 라우트 등록
    register_chat_route(app)      # 추가한 chatbot API 라우트 등록

    return app

# 실행 진입점
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)