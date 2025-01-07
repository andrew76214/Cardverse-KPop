from .extensions import db
import bcrypt
from datetime import datetime

# User Table
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    cn = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), default='user')
    profile_image = db.Column(db.String(255), nullable=True)

    favorites = db.relationship('UserFavorites', back_populates='user', lazy=True)
    cards = db.relationship('UserCards', back_populates='user', lazy=True)
    topic_lists = db.relationship('TopicList', back_populates='user')  # 與 TopicList 表的雙向關聯
    comments = db.relationship('Comments', back_populates='user')  # 與 Comments 表的雙向關聯

    def __init__(self, username, email, password, cn=None, role='user', profile_image=None):
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)
        self.cn = cn
        self.role = role
        self.profile_image = profile_image

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def hash_password(password):
        """加密密碼"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """驗證密碼"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self, include_sensitive=False):
        """轉換為字典，敏感信息可選擇是否包含"""
        user_data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "cn": self.cn,
            "role": self.role,
            "profile_image": self.profile_image,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_sensitive:
            user_data["password_hash"] = self.password_hash
        return user_data


# IP Table
class IP(db.Model):
    __tablename__ = 'ip'
    ip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    characters = db.relationship('IPCharacter', back_populates='ip')

    def to_dict(self):
        return {
            "ip_id": self.ip_id,
            "ip_name": self.ip_name,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }


# IP Characters Table
class IPCharacter(db.Model):
    __tablename__ = 'ip_characters'
    char_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    char_name = db.Column(db.String(100), nullable=False)
    ip_id = db.Column(db.Integer, db.ForeignKey('ip.ip_id'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ip = db.relationship('IP', back_populates='characters')
    merch_items = db.relationship('Merch', back_populates='character')

    def to_dict(self):
        return {
            "char_id": self.char_id,
            "char_name": self.char_name,
            "ip_id": self.ip_id,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }


# Merch Table
class Merch(db.Model):
    __tablename__ = 'merch'
    merch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    char_id = db.Column(db.Integer, db.ForeignKey('ip_characters.char_id'))
    ip_id = db.Column(db.Integer, db.ForeignKey('ip.ip_id'))
    price = db.Column(db.Numeric(10, 2))
    path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    release_at = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    character = db.relationship('IPCharacter', back_populates='merch_items')
    ip = db.relationship('IP')
    favorites = db.relationship('UserFavorites', back_populates='merch')
    tags = db.relationship('MerchTags', back_populates='merch')
    cards = db.relationship('UserCards', back_populates='merch')

    def __init__(self, name, char_id, ip_id, price, path, image_path, release_at):
        self.name = name
        self.char_id = char_id
        self.ip_id = ip_id
        self.price = price
        self.path = path
        self.image_path = image_path
        self.release_at = release_at

    def to_dict(self):
        return {
            "merch_id": self.merch_id,
            "name": self.name,
            "char_id": self.char_id,
            "ip_id": self.ip_id,
            "price": float(self.price) if self.price else 0.0,
            "path": self.path,
            "image_path": self.image_path,
            "release_at": self.release_at,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }


# User Favorites Table
class UserFavorites(db.Model):
    __tablename__ = 'user_favorites'
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='favorites')
    merch = db.relationship('Merch', back_populates='favorites')


# Tags Table
class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    merch_tags = db.relationship('MerchTags', back_populates='tag')


# Merch Tags Table
class MerchTags(db.Model):
    __tablename__ = 'merch_tags'
    merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    merch = db.relationship('Merch', back_populates='tags')
    tag = db.relationship('Tag', back_populates='merch_tags')

# User Cards Table
class UserCards(db.Model):
    __tablename__ = 'user_cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    merch_id = db.Column(db.Integer, db.ForeignKey('merch.merch_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='cards')
    merch = db.relationship('Merch', back_populates='cards')

class TopicList(db.Model):
    """
    第一個表，用來存放討論主題的資訊
    """
    __tablename__ = 'topic_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主鍵 ID
    title = db.Column(db.String(255), nullable=False, index=True)  # 討論主題的標題
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 發表主題的用戶 ID
    user_name = db.Column(db.String(50), nullable=False)  # 發表主題的用戶名稱
    create_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

    user = db.relationship('User', back_populates='topic_lists')  # 與 User 表的雙向關聯
    comments = db.relationship('Comments', back_populates='topic_list')  # 與 Comments 表的雙向關聯

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S") if self.create_at else None,
            "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S") if self.update_at else None
        }



class Comments(db.Model):
    """
    第二個表，用來存放主題的回應資訊
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主鍵 ID
    content = db.Column(db.Text, nullable=False)  # 回應內容
    topic_id = db.Column(db.Integer, db.ForeignKey('topic_list.id'), nullable=False, index=True)  # 對應的主題 ID
    father_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)  # 父回應 ID
    comment_order = db.Column(db.Integer, nullable=False)  # 回應順序
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 發表回應的用戶 ID
    user_name = db.Column(db.String(50), nullable=False)  # 發表回應的用戶名稱
    image_path = db.Column(db.String(255))  # 檔案的儲存路徑

    create_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

    user = db.relationship('User', back_populates='comments')  # 與 User 表的雙向關聯
    topic_list = db.relationship('TopicList', back_populates='comments')  # 與 TopicList 表的雙向關聯
    parent_comment = db.relationship('Comments', remote_side=[id], backref='replies')

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "topic_id": self.topic_id,
            "father_comment_id": self.father_comment_id,
            "comment_order": self.comment_order,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "image_path": self.image_path,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S") if self.create_at else None,
            "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S") if self.update_at else None
        }

    


