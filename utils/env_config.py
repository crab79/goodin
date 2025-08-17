"""
環境變數管理模組
使用 python-dotenv 載入 .env 檔案中的環境變數
"""
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

class Config:
    """應用程式設定類別"""
    
    # 資料庫設定
    DATABASE_URL = os.getenv('DATABASE_URL')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # Flask 設定
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API 設定
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5001/api')
    
    # 安全設定
    JWT_SECRET = os.getenv('JWT_SECRET')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    
    @classmethod
    def validate_config(cls):
        """驗證必要的環境變數是否已設定"""
        required_vars = [
            'DB_NAME', 'DB_USER', 'DB_PASSWORD'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"缺少必要的環境變數: {', '.join(missing_vars)}")
        
        return True

# 建立設定實例
config = Config()

# 驗證設定
try:
    config.validate_config()
    print("✅ 環境變數載入成功")
except ValueError as e:
    print(f"❌ 環境變數設定錯誤: {e}")
    print("請確認 .env 檔案已正確設定")
