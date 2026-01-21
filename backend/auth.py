from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import base64

# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

# БЕЗ bcrypt - используем SHA256 (менее безопасно, но для теста сойдет)
def verify_password(plain_password, hashed_password):
    """Проверяет пароль через SHA256"""
    # Хешируем введенный пароль
    input_hashed = hashlib.sha256(plain_password.encode()).hexdigest()
    return input_hashed == hashed_password

def get_password_hash(password):
    """Хеширует пароль через SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT токен"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Нужно для main.py
ALGORITHM = ALGORITHM