from .extensions import db
import bcrypt
from datetime import datetime


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
    # is_active = db.Column(db.Boolean, default=True, nullable=False)

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
            # "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_sensitive:
            user_data["password_hash"] = self.password_hash
        return user_data
