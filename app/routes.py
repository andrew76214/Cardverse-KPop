from flask import Blueprint, render_template, request, redirect, session, jsonify
from .models import *
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

@main_routes.route('/cardDashboard', methods=['GET', 'POST'])
def cardDashboard():
    return render_template('landing.html')

@main_routes.route('/wishList', methods=['GET', 'POST'])
def wishList():
    return render_template('wishlist.html')
@main_routes.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template('generic.html')
@main_routes.route('/elements', methods=['GET', 'POST'])
def elements():
    return render_template('elements.html')
"""
user
- 創建用戶
- 檢查用戶登錄
"""
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
        # 嘗試從 JSON 或查詢字串中獲取資料
        data = request.get_json() or request.args
        # app.logger.info(f"Received data: {data}")
        
        # 檢查資料完整性
        if not data:
            return jsonify({"status": "fail", "message": "No input data provided"}), 400

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        cn = data.get("cn")

        if not username or not password or not email or not cn:
            return jsonify({"status": "fail", "message": "All fields are required"}), 499

        # 檢查用戶是否已存在
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"status": "fail", "message": "User already exists"}), 409

        # 新建用戶
        # hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=password, email=email, cn=cn)

        # 保存至資料庫
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "message": "User created successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "fail", "message": "Internal Server Error"}), 500


@main_routes.route('/health', methods=['GET'])
def health():
    return {'status': 'healthy'}, 200
"""
IP
- 創建IP
- 獲取所有IP
"""
@main_routes.route('/create_ip', methods=['POST'])
def create_ip():
    try:
        # Try to receive JSON data
        data = request.get_json()

        if not data:
            return jsonify({"status": "fail", "message": "No input data provided"}), 400

        ip_name = data.get("ip_name")
        description = data.get("description")

        if not ip_name:
            return jsonify({"status": "fail", "message": "IP name fields are required"}), 400

        # Check if the IP already exists
        ip = IP.query.filter_by(ip_name=ip_name).first()
        if ip:
            return jsonify({"status": "fail", "message": "IP already exists"}), 409

        # Create a new IP
        new_ip = IP(ip_name=ip_name, description=description)
        # Save to the database
        db.session.add(new_ip)
        db.session.commit()

        return jsonify({"status": "success", "message": "IP created successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")
        # 返回錯誤響應
        return jsonify({"status": "error", "message": "An error occurred", "details": str(e)}), 500
    
@main_routes.route('/get_all_ip', methods=['GET'])
def get_all_ip():
    try:
        ip_list = IP.query.all()
        ip_data = [ip.to_dict() for ip in ip_list]

        return jsonify({"status": "success", "ip": ip_data}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500
"""

Merch
- 獲取所有Merch
"""


@main_routes.route('/get_all_merch', methods=['GET']) 
def get_all_merch():
    try:
        # Retrieve all merchandise from the database
        merch_list = Merch.query.all()

        # Convert each merchandise object to dictionary format
        merch_data = [merch.to_dict() for merch in merch_list]

        # Return the list as JSON
        return jsonify({"status": "success", "merchandise": merch_data}), 200
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"status": "fail", "message": str(e)}), 500

