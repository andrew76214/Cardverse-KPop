from flask import Blueprint, render_template, request, redirect, session, jsonify, send_file
from .models import *
from .extensions import db
import os
import mimetypes
from sqlalchemy import and_
from werkzeug.utils import secure_filename
import uuid
UPLOAD_FOLDER = 'app/static/images/card'  # 定義上傳目錄
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允許的檔案類型
# 確保目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

main_routes = Blueprint('main_routes', __name__)

def process_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()  # 提取副檔名
    new_filename = f"{uuid.uuid4().hex}.{ext}"  # 使用 UUID
    return new_filename

@main_routes.route('/')
def index():
    print(session)
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        # print(user)
        # userdata = user.to_dict()
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
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('cn', None)
    session.pop('role', None)

    return redirect('/')

@main_routes.route('/cardDashboard', methods=['GET', 'POST'])
def cardDashboard():
    return render_template('cardDashboard.html')

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
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        session['cn'] = user.cn
        session['role'] = user.role
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

def create_ip(ip_name):

    # Check if the IP already exists
    ip = IP.query.filter_by(ip_name=ip_name).first()
    description = ""

    # Create a new IP
    new_ip = IP(ip_name=ip_name, description=description)
    # Save to the database
    db.session.add(new_ip)
    db.session.commit()
    
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
def create_character(char_name, ip_id):
    # Check if the character already exists
    character = IPCharacter.query.filter_by(char_name=char_name).first()
    description = ""

    # Create a new character
    new_character = IPCharacter(char_name=char_name, ip_id=ip_id, description=description)
    # Save to the database
    db.session.add(new_character)
    db.session.commit()

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
        merch_list = Merch.query.order_by(Merch.ip_id.asc()).all()
        print(merch_list)
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

        # 模擬查詢數據庫
        if not ip_id:
            return jsonify({"status": "fail", "message": "ip_id is required"}), 400
        elif not character_ids:
            merch_list = Merch.query.filter_by(ip_id=ip_id).all()
        else:
            merch_list = Merch.query.filter(
                            and_(
                                Merch.ip_id == ip_id,
                                Merch.char_id.in_(character_ids)
                            )
                        ).all()
        merch_data = [merch.to_dict() for merch in merch_list]

        return jsonify({"status": "success", "merchandise": merch_data}), 200
    except Exception as e:
        # 返回錯誤響應
        return jsonify({"status": "fail", "message": str(e)}), 500

"""
User_Favorites
"""
@main_routes.route('/get_user_favorites', methods=['GET'])
def get_user_favorites():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        favorites_list = UserFavorites.query.filter_by(user_id=user_id).all()
        favorites_data = [fav.to_dict() for fav in favorites_list]

        return jsonify({"status": "success", "favorites": favorites_data}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@main_routes.route('/create_user_favorite', methods=['POST'])
def create_user_favorite():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        data = request.get_json()
        merch_id = data.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        # 檢查是否已存在
        favorite = UserFavorites.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if favorite:
            return jsonify({"status": "fail", "message": "Favorite already exists"}), 409

        # 新建收藏
        new_favorite = UserFavorites(user_id=user_id, merch_id=merch_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"status": "success", "message": "Favorite created successfully"}), 201
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@main_routes.route('/get_user_favorite_by_id', methods=['GET'])
def get_user_favorite_by_id():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        merch_id = request.args.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        favorite = UserFavorites.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if not favorite:
            return jsonify({"status": "success", "is_favorite": False}), 200

        return jsonify({"status": "success", "is_favorite": True}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500
    
    
@main_routes.route('/delete_user_favorite', methods=['POST'])
def delete_user_favorite():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        data = request.get_json()
        merch_id = data.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        # 查找收藏
        favorite = UserFavorites.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if not favorite:
            return jsonify({"status": "fail", "message": "Favorite not found"}), 404

        # 刪除收藏
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"status": "success", "message": "Favorite deleted successfully"}), 200
    except Exception as e:
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
    
"""
search_mearch(user_favorite version)
"""
@main_routes.route('/get_user_favorites_from_merch', methods=['GET'])
def get_user_favorites_from_merch():
    try:
        print(session)
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "User not logged in"}), 401
        # 使用 JOIN 查詢 user_favorites 與 merch 的關聯資料
        favorites = db.session.query(Merch).join(UserFavorites).filter(UserFavorites.user_id == user_id).order_by(Merch.ip_id.asc()).all()

        # 將結果轉換為 JSON 格式
        result = [merch.to_dict() for merch in favorites]
        return jsonify({"status": "success", "merchandise": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@main_routes.route('/get_merch_by_id_user_favorite_ver', methods=['POST'])
def get_merch_by_id_user_favorite_ver():
    try:
        user_id = session.get('user_id')
        # 從請求的 JSON 數據中獲取 ip_id 和 char_id
        data = request.json
        ip_id = data.get('ip_id')
        character_ids = data.get('character_ids', [])

        # 模擬查詢數據庫
        if not ip_id:
            return jsonify({"status": "fail", "message": "ip_id is required"}), 400
        elif not character_ids:
            favorites = db.session.query(Merch).join(UserFavorites).filter(
                            UserFavorites.user_id == user_id,
                            Merch.ip_id == ip_id
                        ).all()
        else:
            # 查詢用戶收藏的商品資料，並篩選特定角色
            favorites = db.session.query(Merch).join(UserFavorites).filter(
                            UserFavorites.user_id == user_id,
                            Merch.char_id.in_(character_ids)
                        ).all()

        
        # 將查詢結果轉換為 JSON 格式
        result = [merch.to_dict() for merch in favorites]
        return jsonify({"status": "success", "merchandise": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main_routes.route('/create_merch', methods=['POST'])
def create_merch():
    try:
        file = request.files.get('photo')  # 獲取上傳的檔案
        data = request.form  # 獲取其他的表單數據

        if not file or file.filename == '':
            return jsonify({"status": "error", "message": "No file provided"}), 400

        # 驗證檔案類型
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return jsonify({"status": "error", "message": "Invalid file type"}), 400

        # 使用 secure_filename 防止檔案名注入
        # filename = secure_filename(file.filename)
        # print("filename")
        # print(filename)
        filename = process_filename(file.filename)

        filepath = os.path.join(UPLOAD_FOLDER, filename)


        # 儲存檔案到伺服器
        file.save(filepath)
        
        if not data:
            return jsonify({"status": "error", "message": "No input data provided"}), 400
        print(data)
        # print(file)
        # 檢查必要欄位
        required_fields = ['ipName', 'charname']
        for field in required_fields:
            if field not in data:
                return jsonify({"status": "error", "message": f"Missing {field}"}), 400
        
        # 檢查 IP 是否存在
        ip_instance = IP.query.filter_by(ip_name=data['ipName']).first()
        if not ip_instance:
            create_ip(data['ipName'])
            ip_instance = IP.query.filter_by(ip_name=data['ipName']).first()
        ipdata = ip_instance.to_dict()
        print("ipdata")
        print(ipdata)

        # 檢查角色是否存在
        char_instance = IPCharacter.query.filter_by(ip_id=ipdata['ip_id'], char_name=data['charname']).first()
        if not char_instance:
            create_character(data['charname'], ipdata['ip_id'])
            char_instance = IPCharacter.query.filter_by(ip_id=ipdata['ip_id'], char_name=data['charname']).first()
        chardata = char_instance.to_dict()
        print("chardata")
        print(chardata)
        merch_name = data['charname'] + "_" + data['vol'] + "_" + data['version']
        # 檢查商品是否存在
        merch_instance = Merch.query.filter_by(ip_id=ipdata['ip_id'], char_id=chardata['char_id'], name=merch_name).first()
        if merch_instance:
            return jsonify({"status": "error", "message": "Merchandise already exists"}), 409
        # 創建新商品
        new_merch = Merch(
            ip_id=ipdata['ip_id'],
            char_id=chardata['char_id'],
            name=merch_name,
            price=0,
            path=data['path'],
            image_path=filename,
            release_at=data['releaseAt']
        )

        # 保存至資料庫
        db.session.add(new_merch)
        db.session.commit()

        return jsonify({"status": "success", "merchID": new_merch.to_dict()['merch_id']}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
"""
search_mearch(user_card version)
"""
@main_routes.route('/get_user_cards_from_merch', methods=['GET'])
def get_user_cards_from_merch():
    try:
        print(session)
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "User not logged in"}), 401
        # 使用 JOIN 查詢 user_cards 與 merch 的關聯資料
        cards = db.session.query(Merch).join(UserCards).filter(UserCards.user_id == user_id).order_by(Merch.ip_id.asc()).all()

        # 將結果轉換為 JSON 格式
        result = [merch.to_dict() for merch in cards]
        return jsonify({"status": "success", "merchandise": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@main_routes.route('/get_merch_by_id_user_card_ver', methods=['POST'])
def get_merch_by_id_user_card_ver():
    try:
        user_id = session.get('user_id')
        # 從請求的 JSON 數據中獲取 ip_id 和 char_id
        data = request.json
        ip_id = data.get('ip_id')
        character_ids = data.get('character_ids', [])

        # 模擬查詢數據庫
        if not ip_id:
            return jsonify({"status": "fail", "message": "ip_id is required"}), 400
        elif not character_ids:
            cards = db.session.query(Merch).join(UserFavorites).filter(
                            UserCards.user_id == user_id,
                            Merch.ip_id == ip_id
                        ).all()
        else:
            # 查詢用戶收藏的商品資料，並篩選特定角色
            cards = db.session.query(Merch).join(UserCards).filter(
                        UserCards.user_id == user_id,
                        Merch.char_id.in_(character_ids)
                    ).all()

        

        # 將查詢結果轉換為 JSON 格式
        result = [merch.to_dict() for merch in cards]
        return jsonify({"status": "success", "merchandise": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

"""
User_Cards
"""
@main_routes.route('/get_user_cards', methods=['GET'])
def get_user_cards():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        cards_list = UserCards.query.filter_by(user_id=user_id).all()
        cards_data = [fav.to_dict() for fav in cards_list]

        return jsonify({"status": "success", "cards": cards_data}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@main_routes.route('/create_user_card', methods=['POST'])
def create_user_card():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        data = request.get_json()
        merch_id = data.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        # 檢查是否已存在
        card = UserCards.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if card:
            return jsonify({"status": "fail", "message": "Card already exists"}), 409

        # 新建收藏
        new_card = UserCards(user_id=user_id, merch_id=merch_id)
        db.session.add(new_card)
        db.session.commit()

        return jsonify({"status": "success", "message": "Card created successfully"}), 201
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500

@main_routes.route('/get_user_card_by_id', methods=['GET'])
def get_user_card_by_id():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        merch_id = request.args.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        card = UserCards.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if not card:
            return jsonify({"status": "success", "is_card": False}), 200

        return jsonify({"status": "success", "is_card": True}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500
    
    
@main_routes.route('/delete_user_card', methods=['POST'])
def delete_user_card():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "fail", "message": "User not logged in"}), 401

        data = request.get_json()
        merch_id = data.get('merch_id')
        if not merch_id:
            return jsonify({"status": "fail", "message": "merch_id is required"}), 400

        # 查找收藏
        card = UserCards.query.filter_by(user_id=user_id, merch_id=merch_id).first()
        if not card:
            return jsonify({"status": "fail", "message": "Card not found"}), 404

        # 刪除收藏
        db.session.delete(card)
        db.session.commit()

        return jsonify({"status": "success", "message": "Card deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)}), 500
