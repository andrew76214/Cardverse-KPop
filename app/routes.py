from flask import Blueprint, render_template, request, redirect, session, jsonify
from .models import User
from .extensions import db

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    print(session)
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        print(user)
        return render_template('index.html', user=user)
    return render_template('index.html', user=None)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
    
@main_routes.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@main_routes.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
    print(user)
    return render_template('dashboard.html', user=user)  # 傳遞給模板
    # return redirect('/login')

@main_routes.route('/check_user_login', methods=['POST'])
def check_user_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = user.username
        print(session)
        # 返回用戶的完整 JSON 資料
        return jsonify(user.to_dict())
    else:
        return jsonify({"status": "fail", "message": "Invalid username or password"}), 401



@main_routes.route('/create_user', methods=['POST'])
def create_user():
    try:
        # 嘗試接收 JSON 資料
        data = request.get_json()

        # 檢查資料完整性
        if not data:
            return jsonify({"status": "fail", "message": "No input data provided"}), 400

        username = data.get("username")
        password = data.get("password")  # 必須處理密碼！
        email = data.get("email")
        cn = data.get("cn")

        if not username or not password or not email or not cn:
            return jsonify({"status": "fail", "message": "All fields are required"}), 400

        # 檢查用戶是否已存在
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"status": "fail", "message": "User already exists"}), 409

        # 新建用戶 (記得處理密碼加密)
        new_user = User(username=username, password=password, email=email, cn=cn)
        # 保存至資料庫
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User created successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")  # 打印詳細錯誤日誌
        return jsonify({"status": "fail", "message": "Internal Server Error"}), 500

@main_routes.route('/health', methods=['GET'])
def health():
    return {'status': 'healthy'}, 200