import requests
import logging
from typing import Optional
from .config import OLLAMA_BASE_URL, DEFAULT_MODEL, SYSTEM_PROMPT_TEMPLATE

# Настройка логирования
logger = logging.getLogger(__name__)

class LLMService:
    """Сервис для общения с языковой моделью (Ollama)."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or DEFAULT_MODEL
        logger.info(f"LLMService инициализирован: {self.base_url}, модель: {self.model}")

    def _build_prompt(self, session_context: str, current_situation: str, player_input: str) -> str:
        """Создает промпт для AI Мастера на основе шаблона."""
        prompt = SYSTEM_PROMPT_TEMPLATE.format(
            session_context=session_context,
            current_situation=current_situation
        )
        
        # Добавляем последний ввод игрока
        full_prompt = f"{prompt}\n\nИгрок: {player_input}\n\nМастер:"
        return full_prompt

    def generate_response(
        self, 
        session_context: str = "", 
        current_situation: str = "", 
        player_input: str = "Начни приключение!"
    ) -> str:
        """
        Главный метод. Формирует промпт и отправляет его в Ollama для генерации ответа Мастера.

        Args:
            session_context: История или ключевые факты сессии.
            current_situation: Текущее состояние (локация, NPC вокруг).
            player_input: Что сказал или сделал игрок.

        Returns:
            Ответ AI Мастера (строка).

        Raises:
            ConnectionError: Если Ollama недоступен.
            Exception: При других ошибках.
        """
        try:
            # 1. Собираем промпт
            prompt = self._build_prompt(session_context, current_situation, player_input)
            logger.debug(f"Сформирован промпт длиной {len(prompt)} символов")
            
            # 2. Подготовка запроса к Ollama API
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,  # Получаем сразу весь ответ
                "options": {
                    "temperature": 0.8,  # Креативность (0.0-1.0)
                    "top_p": 0.9,       # Разнообразие ответов
                    "num_predict": 1024  # Максимальная длина ответа
                }
            }
            
            # 3. Отправка запроса
            logger.info(f"Отправка запроса к {url} с моделью {self.model}")
            response = requests.post(url, json=payload, timeout=60)  # 60 секунд таймаут
            response.raise_for_status()  # Проверяем HTTP ошибки
            
            # 4. Обработка ответа
            result = response.json()
            ai_response = result.get("response", "").strip()
            
            # 5. Очистка ответа (иногда модель повторяет промпт)
            if "Мастер:" in ai_response:
                ai_response = ai_response.split("Мастер:")[-1].strip()
            
            logger.info(f"Получен ответ длиной {len(ai_response)} символов")
            return ai_response
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Не удалось подключиться к Ollama по адресу {self.base_url}. Убедитесь, что Ollama запущен."
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        except requests.exceptions.Timeout:
            error_msg = "Таймаут при обращении к Ollama. Модель долго генерирует ответ."
            logger.error(error_msg)
            return "Мастер задумался... (таймаут генерации)"
        except Exception as e:
            error_msg = f"Ошибка при генерации ответа: {str(e)}"
            logger.error(error_msg)
            return f"Мастер растерялся! (ошибка: {str(e)})"

    def test_connection(self) -> bool:
        """Проверяет, доступен ли Ollama API."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

# Создаем глобальный экземпляр сервиса для удобства
llm_service = LLMService()