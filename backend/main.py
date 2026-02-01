from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from typing import List
from jose import JWTError, jwt
import models
from database import engine, get_db
import schemas, crud, auth
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, get_current_user
from routers import chat

# Создаем все таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI D&D Companion API",
    description="Backend для игры в D&D с AI Мастером",
    version="0.3.0"
)

# Настройка OAuth2 для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ----- Эндпоинты -----
@app.get("/")
def read_root():
    return {"message": "AI D&D Backend успешно запущен! 🐉"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    """Тестовый эндпоинт для проверки подключения к БД"""
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {
            "status": "success", 
            "message": "База данных работает корректно",
            "db_test": result[0]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    # Проверяем, не занят ли email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Проверяем, не занят ли username
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя пользователя уже занято"
        )
    
    # Создаем пользователя
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Вход пользователя и получение JWT токена"""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Получить информацию о текущем пользователе"""
    return current_user

# ----- Эндпоинты игровых сессий (базовые) -----
@app.post("/sessions", response_model=schemas.GameSessionResponse)
def create_session(
    session: schemas.GameSessionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую игровую сессию"""
    return crud.create_game_session(db=db, session=session, user_id=current_user.id)

@app.get("/sessions", response_model=List[schemas.GameSessionResponse])
def read_sessions(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все сессии текущего пользователя"""
    sessions = crud.get_user_sessions(db, user_id=current_user.id, skip=skip, limit=limit)
    return sessions

# Подключаем роутер чата
app.include_router(chat.router)