#!/usr/bin/env python3
"""
Тест эндпоинта чата с AI Мастером
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "gandalf@middle-earth.com"
TEST_PASSWORD = "youshallnotpass"

def get_auth_token():
    """Получить JWT токен для тестового пользователя"""
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Токен получен")
        return token
    else:
        print(f"❌ Ошибка получения токена: {response.status_code}")
        print(response.text)
        return None

def create_test_session(token):
    """Создать тестовую сессию"""
    headers = {"Authorization": f"Bearer {token}"}
    
    session_data = {
        "title": "Тестовое приключение",
        "character_data": {"name": "Теоден", "class": "Воин", "level": 1},
        "world_context": "Земли Рохана, время великой войны"
    }
    
    response = requests.post(
        f"{BASE_URL}/sessions",
        json=session_data,
        headers=headers
    )
    
    if response.status_code == 200:
        session = response.json()
        print(f"✅ Сессия создана: {session['title']} (ID: {session['id']})")
        return session["id"]
    else:
        print(f"❌ Ошибка создания сессии: {response.status_code}")
        print(response.text)
        return None

def test_chat_endpoint(token, session_id):
    """Протестировать эндпоинт /chat"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🧪 Тестирование чата с AI Мастером...")
    print(f"   ID сессии: {session_id}")
    
    # Первое сообщение
    chat_data = {
        "session_id": session_id,
        "player_input": "Я вхожу в древний лес. Что я вижу вокруг?",
        "generate_image": False
    }
    
    print(f"   Отправка: {chat_data['player_input']}")
    
    response = requests.post(
        f"{BASE_URL}/chat/",
        json=chat_data,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result["message"]["content"]
        print(f"   ✅ Ответ AI получен ({len(ai_response)} символов):")
        print("-" * 60)
        print(ai_response[:500] + "..." if len(ai_response) > 500 else ai_response)
        print("-" * 60)
        
        # Второе сообщение для проверки контекста
        print(f"\n   Второй запрос: 'Я иду глубже в лес'")
        chat_data["player_input"] = "Я иду глубже в лес"
        
        response2 = requests.post(
            f"{BASE_URL}/chat/",
            json=chat_data,
            headers=headers
        )
        
        if response2.status_code == 200:
            result2 = response2.json()
            ai_response2 = result2["message"]["content"]
            print(f"   ✅ Второй ответ получен:")
            print("-" * 60)
            print(ai_response2[:500] + "..." if len(ai_response2) > 500 else ai_response2)
            print("-" * 60)
            print("\n🎉 Эндпоинт /chat работает корректно!")
        else:
            print(f"   ❌ Ошибка второго запроса: {response2.status_code}")
            print(response2.text)
            
    else:
        print(f"   ❌ Ошибка: {response.status_code}")
        print(response.text)

def main():
    print("🤖 Тестирование эндпоинта /chat")
    print("=" * 60)
    
    # 1. Получаем токен
    token = get_auth_token()
    if not token:
        return
    
    # 2. Создаем сессию
    session_id = create_test_session(token)
    if not session_id:
        return
    
    # 3. Тестируем чат
    test_chat_endpoint(token, session_id)

if __name__ == "__main__":
    main()