from flask import Flask
from routes import register_routes

# 초기 실행
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testsecretkey'
    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)