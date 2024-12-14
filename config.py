import os
from dotenv import load_dotenv

# 載入 .env 文件
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

