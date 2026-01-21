# Схема базы данных AI D&D Companion

## 1. Таблица `users` (Пользователи)
Хранит информацию о зарегистрированных пользователях.
*   `id` (INTEGER, PRIMARY KEY) - уникальный номер пользователя
*   `username` (VARCHAR) - имя для входа (например, "GandalfTheGray")
*   `email` (VARCHAR, UNIQUE) - электронная почта
*   `hashed_password` (VARCHAR) - зашифрованный пароль (НИКОГДА не храним открытый пароль!)
*   `created_at` (TIMESTAMP) - дата регистрации
*   `credits` (INTEGER, default=10) - сколько кредитов осталось на генерацию изображений
*   `subscription_tier` (VARCHAR, default='free') - уровень подписки: 'free', 'premium'

## 2. Таблица `game_sessions` (Игровые сессии)
Каждая игра пользователя — это отдельная сессия.
*   `id` (INTEGER, PRIMARY KEY) - уникальный номер сессии
*   `user_id` (INTEGER, FOREIGN KEY -> users.id) - кто владелец сессии
*   `title` (VARCHAR, default='Новое приключение') - название сессии
*   `character_data` (JSON, default='{}') - **ЛИСТ ПЕРСОНАЖА в формате JSON**. Пример: {"name": "Эльринд", "class": "Воин", "hp": 45, "inventory": ["меч", "щит"]}
*   `world_context` (TEXT, default='') - дополнительный контекст мира от Мастера
*   `created_at` (TIMESTAMP) - дата создания
*   `updated_at` (TIMESTAMP) - дата последнего действия

## 3. Таблица `messages` (Сообщения в чате)
Каждое сообщение в чате игры сохраняется здесь.
*   `id` (INTEGER, PRIMARY KEY) - уникальный номер сообщения
*   `session_id` (INTEGER, FOREIGN KEY -> game_sessions.id) - к какой сессии относится
*   `role` (VARCHAR) - кто отправил: 'user' (игрок), 'assistant' (AI Мастер), 'system'
*   `content` (TEXT) - текст сообщения
*   `image_url` (VARCHAR, nullable) - URL сгенерированной картинки (если есть)
*   `timestamp` (TIMESTAMP) - время отправки