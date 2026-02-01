from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
import schemas, crud
from auth import get_current_user
from models import User, GameSession
from services.llm_service import llm_service

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.ChatResponse)
async def chat_with_master(
    chat_request: schemas.ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Основной эндпоинт для общения с AI Мастером.
    
    1. Проверяет, что сессия принадлежит пользователю
    2. Сохраняет сообщение игрока
    3. Генерирует контекст для AI
    4. Получает ответ от AI Мастера
    5. Сохраняет ответ и возвращает его
    """
    
    # 1. Проверяем, что сессия существует и принадлежит пользователю
    session = db.query(GameSession).filter(
        GameSession.id == chat_request.session_id,
        GameSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не найдена или у вас нет к ней доступа"
        )
    
    # 2. Сохраняем сообщение игрока
    player_message = schemas.MessageCreate(
        content=chat_request.player_input,
        role="user"
    )
    crud.create_message(db, player_message, chat_request.session_id)
    
    # 3. Подготавливаем контекст для AI
    # Получаем последние сообщения для контекста
    last_messages = crud.get_last_messages(db, chat_request.session_id, limit=10)
    
    # Формируем историю диалога
    message_history = ""
    for msg in reversed(last_messages):  # reversed чтобы хронологический порядок
        role_name = "Игрок" if msg.role == "user" else "Мастер"
        message_history += f"{role_name}: {msg.content}\n"
    
    # 4. Генерируем ответ AI Мастера
    try:
        ai_response = llm_service.generate_response(
            session_context=session.world_context or "",
            current_situation=message_history or "Начало приключения",
            player_input=chat_request.player_input
        )
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа AI: {e}")
        ai_response = "Мастер временно недоступен. Попробуйте позже."
    
    # 5. Сохраняем ответ AI
    ai_message = schemas.MessageCreate(
        content=ai_response,
        role="assistant"
    )
    saved_ai_message = crud.create_message(db, ai_message, chat_request.session_id)
    
    # 6. Обновляем время сессии
    session.updated_at = db.execute("SELECT CURRENT_TIMESTAMP").scalar()
    db.commit()
    
    return schemas.ChatResponse(
        message=saved_ai_message
    )

@router.get("/history/{session_id}", response_model=List[schemas.MessageResponse])
async def get_chat_history(
    session_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить историю сообщений сессии"""
    
    # Проверяем доступ к сессии
    session = db.query(GameSession).filter(
        GameSession.id == session_id,
        GameSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия не найдена или у вас нет к ней доступа"
        )
    
    messages = crud.get_session_messages(db, session_id, limit)
    return messages