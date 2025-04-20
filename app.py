import http.client
import json
from flask import Flask, render_template, request

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# Полный список сервисов, разделенный на 5 страниц
routes = {
    "ru": [
        ["instagram", "tiktok", "douyin", "capcut", "threads", "facebook", "kuaishou"],
        ["espn", "pinterest", "imgur", "ifunny", "reddit", "youtube", "twitter"],
        ["vimeo", "snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr"],
        ["febspot", "9gag", "rumble", "ted", "sohutv", "xiaohongshu", "ixigua"],
        ["meipai", "bluesky", "soundcloud", "mixcloud", "spotify", "zingmp3", "bandcamp"]
    ],
    "en": [
        ["instagram", "tiktok", "douyin", "capcut", "threads", "facebook", "kuaishou"],
        ["espn", "pinterest", "imgur", "ifunny", "reddit", "youtube", "twitter"],
        ["vimeo", "snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr"],
        ["febspot", "9gag", "rumble", "ted", "sohutv", "xiaohongshu", "ixigua"],
        ["meipai", "bluesky", "soundcloud", "mixcloud", "spotify", "zingmp3", "bandcamp"]
    ],
    "es": [
        ["instagram", "tiktok", "douyin", "capcut", "threads", "facebook", "kuaishou"],
        ["espn", "pinterest", "imgur", "ifunny", "reddit", "youtube", "twitter"],
        ["vimeo", "snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr"],
        ["febspot", "9gag", "rumble", "ted", "sohutv", "xiaohongshu", "ixigua"],
        ["meipai", "bluesky", "soundcloud", "mixcloud", "spotify", "zingmp3", "bandcamp"]
    ],
    "zh": [
        ["instagram", "tiktok", "douyin", "capcut", "threads", "facebook", "kuaishou"],
        ["espn", "pinterest", "imgur", "ifunny", "reddit", "youtube", "twitter"],
        ["vimeo", "snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr"],
        ["febspot", "9gag", "rumble", "ted", "sohutv", "xiaohongshu", "ixigua"],
        ["meipai", "bluesky", "soundcloud", "mixcloud", "spotify", "zingmp3", "bandcamp"]
    ]
}

# Главная страница
@app.route('/')
def index():
    return render_template("index.html")

# SEO-страницы для каждого языка и сервиса
for lang, services_list in routes.items():
    for i, services in enumerate(services_list):
        route = f"/{lang}/page{i+1}"
        def make_view(services=services, lang=lang):
            def view():
                return render_template("seo_page.html", services=services, lang=lang)
            return view
        app.add_url_rule(route, f"{lang}_page{i+1}", make_view())

# Страница для скачивания
from flask import Flask, render_template, request
import http.client
import json

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "URL не указан", 400

    # Запрос к API для получения ссылки на видео
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

    if not data:
        return "Не удалось получить данные", 500

    # Преобразуем ответ в JSON и получаем ссылку на скачивание
    response = json.loads(data.decode('utf-8'))
    video_url = response.get('medias', [{}])[0].get('url', '')
    
    if not video_url:
        return "Не удалось получить ссылку для скачивания. Попробуйте другую ссылку.", 400

    # Отображаем результат с кнопкой для скачивания
    return render_template('result.html', video_url=video_url, title=response.get('title', 'Видео'))

if __name__ == '__main__':
    app.run(debug=True)
