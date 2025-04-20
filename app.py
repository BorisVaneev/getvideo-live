from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import http.client
import json
import requests

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# Сервисы по страницам
ALL_SERVICES = {
    "page1": ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "vimeo"],
    "page2": ["reddit", "linkedin", "pinterest", "tumblr", "vimeo", "soundcloud", "spotify"],
    "page3": ["soundcloud", "spotify", "mixcloud", "bandcamp", "zingmp3", "vimeo", "youtube"],
    "page4": ["douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "twitter", "vimeo"],
    "page5": ["snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr", "9gag"]
}

# Сервисы для разных языков
SERVICES = {
    "ru": ALL_SERVICES,
    "en": ALL_SERVICES,
    "es": ALL_SERVICES,
    "zh": ALL_SERVICES
}

# Главная страница
@app.route('/')
def index():
    return render_template("index.html")

# Динамически создаем страницы для каждого языка и сервисов
for lang, pages in SERVICES.items():
    for page, services in pages.items():
        route = f"/{lang}/{page}"
        def make_view(p=page, s=services, l=lang):
            def view():
                return render_template("seo_page.html", services=s, lang=l, page=p)
            return view
        app.add_url_rule(route, f"{lang}_{page}", make_view())

# Страница загрузки
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "URL не указан", 400

    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    payload = json.dumps({"url": video_url})
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/social/autolink", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    # Предположим, что мы получаем данные, которые нужно отобразить
    try:
        result = json.loads(data)
        return render_template("result.html", result=result)
    except Exception as e:
        return f"Ошибка обработки данных: {e}"

# Страница для скачивания видео
@app.route('/download_video', methods=['GET'])
def download_video():
    # Получаем ссылку на видео из параметра запроса
    video_url = request.args.get('url')
    
    # Пытаемся загрузить видео с источника
    response = requests.get(video_url, stream=True)
    
    # Проверяем, что запрос успешен
    if response.status_code == 200:
        # Устанавливаем заголовки для скачивания
        headers = {
            'Content-Disposition': 'attachment; filename="video.mp4"',
            'Content-Type': 'video/mp4',
        }
        
        # Отправляем файл с корректными заголовками
        return Response(response.iter_content(chunk_size=1024), headers=headers)

    return "Error: Could not fetch video", 400

if __name__ == '__main__':
    app.run(debug=True)
