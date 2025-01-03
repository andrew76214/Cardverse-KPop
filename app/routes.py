from flask import Blueprint, render_template, request, redirect, session, jsonify, send_file
from .models import *
from .extensions import db
import os
import mimetypes

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

        return jsonify({"status": "success", "ip_data": ip_data}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@main_routes.route('/get_ip_by_id', methods=['GET'])
def get_ip_by_id():
    ip_id = request.args.get('ip_id')
    if not ip_id:
        return jsonify({"status": "fail", "message": "ip_id is required"}), 400

    ip = IP.query.filter_by(ip_id=ip_id).first()
    if not ip:
        return jsonify({"status": "fail", "message": "IP not found"}), 404

    return jsonify({"status": "success", "ip_data": ip.to_dict()}), 200
"""
IP_characters
"""
@main_routes.route('/get_character_by_ipid', methods=['GET'])
def get_character_by_ipid():
    try:
        ip_id = request.args.get('ip_id')
        if not ip_id:
            return jsonify({"status": "fail", "message": "ip_id is required"}), 400

        character_list = IPCharacter.query.filter_by(ip_id=ip_id).all()
        character_data = [char.to_dict() for char in character_list]
        return jsonify({"status": "success", "characters": character_data}), 200
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

@main_routes.route('/get_merch_by_id', methods=['POST'])
def get_merch_by_id():
    try:
        data = request.json
        ip_id = data.get('ip_id')
        character_ids = data.get('character_ids', [])

        # 模擬處理數據
        print(f"Received IP ID: {ip_id}")
        print(f"Received Character IDs: {character_ids}")

        # 返回成功響應
        return jsonify({"status": "success", "message": "Data processed successfully"}), 200
    except Exception as e:
        # 返回錯誤響應
        return jsonify({"status": "fail", "message": str(e)}), 500


"""
images
"""
# 設定圖片存放的目錄
IMAGE_FOLDER = os.path.join(os.getcwd(), "app/static/images/card")

# 確保圖片目錄存在
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

@main_routes.route('/get_image', methods=['GET'])
def get_image():
    """
    動態獲取圖片 API
    Query Params:
    - image_path: 前端提供的圖片相對路徑 (e.g., "images/card/miku_10c_beforetraining.jpg")
    """
    try:
        # 從查詢參數中獲取圖片路徑
        image_path = request.args.get('image_path')
        if not image_path:
            return jsonify({"status": "fail", "message": "No image_path provided"}), 400

        # 確定圖片的完整路徑
        full_image_path = os.path.join(IMAGE_FOLDER, image_path)
        print(f"Iamge Folder Path: {IMAGE_FOLDER}")
        print(f"Requested Image Path: {full_image_path}")

        # 檢查圖片是否存在
        if not os.path.isfile(full_image_path):
            return jsonify({"status": "fail", "message": "Image not found"}), 404

        # 返回圖片文件
        # return send_file(full_image_path, mimetype='image/jpeg')  # 根據實際圖片類型設置 mimetype
        return send_file(full_image_path, mimetype=mimetypes.guess_type(full_image_path)[0])
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500