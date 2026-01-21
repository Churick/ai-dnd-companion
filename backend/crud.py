from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash, verify_password

# ----- User CRUD -----
def get_user_by_email(db: Session, email: str):
    """Найти пользователя по email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Найти пользователя по username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """Аутентификация пользователя"""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# ----- Game Session CRUD -----
def create_game_session(db: Session, session: schemas.GameSessionCreate, user_id: int):
    """Создать новую игровую сессию"""
    db_session = models.GameSession(**session.dict(), user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_sessions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Получить сессии пользователя"""
    return db.query(models.GameSession)\
        .filter(models.GameSession.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()