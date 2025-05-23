# advanced/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import mysql.connector
import bcrypt

auth_bp = Blueprint('auth',
                    __name__,
                    url_prefix="/auth",
                    template_folder="/templates",
                    static_folder="/static")

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    # 로그인 화면
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        try:
            # DB 연결
            conn = mysql.connector.connect(
                host="192.168.0.64",
                user="advanced_db",
                password="human_advanced",
                database="advanced_project"
            )
            cursor = conn.cursor(dictionary=True)

            # 유저 정보 DB 조회
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # 로그인 성공 - 세션에 정보 저장
                session['user_id'] = user['id']
                session['nickname'] = user.get('nickname') or username['username'] # 닉네임 없으면 username 사용
                session['profile_image'] = user.get('profile_image') or "images/default_profile.png"
                print(user.get('profile_image'))

                return redirect(url_for("main.index"))
            else:
                flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")

        except mysql.connector.Error as err:
            print("DB 오류:", err)
            flash("서버 오류가 발생했습니다.", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template("auth/login.html")

@auth_bp.route('/logout')
def logout():
    # 로그아웃 처리
    session.clear()
    return redirect( url_for("main.index", alert="로그아웃 되었습니다.") )

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    # 회원가입 처리
    pass