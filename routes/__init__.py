from flask import Blueprint

# 라우트 등록
def register_routes(app):
    from .main_routes import main_bp
    from .auth_routes import auth_bp
    from .chat_routes import chat_bp

    # 등록할 라우트 리스트
    blueprints = [main_bp, auth_bp, chat_bp]

    for bp in blueprints:
        app.register_blueprint(bp)