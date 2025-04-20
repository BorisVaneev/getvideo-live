# getvideo-live

Простой Flask‑сервис для скачивания видео через RapidAPI.

## Запуск локально

1. Клонировать репозиторий  
2. Создать и активировать виртуальное окружение:  
   `python3 -m venv venv && source venv/bin/activate`  
3. Установить зависимости:  
   `pip install -r requirements.txt`  
4. Запустить:  
   `python app.py`  

## Деплой

- Развернуть на любом хостинге (Hetzner, Render и т.д.)  
- Настроить переменную окружения `RAPIDAPI_KEY`

