#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы AI сервиса.
Запуск: python test_llm.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import llm_service

def test_ai_master():
    """Тестируем работу AI Мастера."""
    
    print("🤖 Тестирование AI D&D Мастера...")
    print("=" * 50)
    
    # 1. Проверяем подключение к Ollama
    print("1. Проверка подключения к Ollama...")
    if llm_service.test_connection():
        print("   ✅ Ollama доступен!")
    else:
        print("   ❌ Ollama недоступен! Убедитесь, что он запущен.")
        print("   Команда для запуска: ollama serve")
        return
    
    # 2. Первый тест - начало приключения
    print("\n2. Тест: Начало нового приключения...")
    print(f"   Модель: {llm_service.model}")
    
    try:
        response = llm_service.generate_response(
            session_context="Новая игра, персонаж - Эльринд, эльфийский воин",
            current_situation="Таверна 'Веселый гном', вечер",
            player_input="Я осматриваюсь по таверне. Кто здесь есть?"
        )
        
        print(f"   ✅ Ответ получен ({len(response)} символов):")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        # 3. Второй тест - продолжение диалога
        print("\n3. Тест: Продолжение диалога...")
        
        follow_up = llm_service.generate_response(
            session_context="Эльринд в таверне, познакомился со странным стариком",
            current_situation="Старик предлагает опасное задание",
            player_input="Я спрашиваю у старика, какая награда ждет меня за выполнение задания"
        )
        
        print(f"   ✅ Ответ получен ({len(follow_up)} символов):")
        print("-" * 50)
        print(follow_up)
        print("-" * 50)
        
        print("\n🎉 Все тесты пройдены успешно! AI Мастер готов к работе.")
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

if __name__ == "__main__":
    test_ai_master()