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
    release_at = db.Column(db.DateTime)
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
            "release_at": self.release_at.strftime("%Y-%m-%d %H:%M:%S") if self.release_at else None,
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
