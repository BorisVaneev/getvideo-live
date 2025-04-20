from flask import Flask, render_template, request
import http.client
import json

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# Разделим сервисы на страницы (5 страниц по 7 сервисов)
services_dict = {
    "ru": [
        ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "linkedin"],
        ["pinterest", "tumblr", "vimeo", "soundcloud", "spotify", "mixcloud", "bandcamp"],
        ["zingmp3", "douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "likee"],
        ["dailymotion", "sharechat", "febspot", "9gag", "rumble", "ted", "sohutv"],
        ["bluesky", "soundcloud", "meipai", "mixcloud", "spotify", "bandcamp", "tiktok"]
    ],
    "en": [
        ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "linkedin"],
        ["pinterest", "tumblr", "vimeo", "soundcloud", "spotify", "mixcloud", "bandcamp"],
        ["zingmp3", "douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "likee"],
        ["dailymotion", "sharechat", "febspot", "9gag", "rumble", "ted", "sohutv"],
        ["bluesky", "soundcloud", "meipai", "mixcloud", "spotify", "bandcamp", "tiktok"]
    ],
    "es": [
        ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "linkedin"],
        ["pinterest", "tumblr", "vimeo", "soundcloud", "spotify", "mixcloud", "bandcamp"],
        ["zingmp3", "douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "likee"],
        ["dailymotion", "sharechat", "febspot", "9gag", "rumble", "ted", "sohutv"],
        ["bluesky", "soundcloud", "meipai", "mixcloud", "spotify", "bandcamp", "tiktok"]
    ],
    "zh": [
        ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "linkedin"],
        ["pinterest", "tumblr", "vimeo", "soundcloud", "spotify", "mixcloud", "bandcamp"],
        ["zingmp3", "douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "likee"],
        ["dailymotion", "sharechat", "febspot", "9gag", "rumble", "ted", "sohutv"],
        ["bluesky", "soundcloud", "meipai", "mixcloud", "spotify", "bandcamp", "tiktok"]
    ]
}

# Создаем страницы для каждого языка и сервиса
for lang, service_groups in services_dict.items():
    for idx, services in enumerate(service_groups):
        route = f"/{lang}/page{idx + 1}"
        def make_view(services=services, lang=lang):
            def view():
                return render_template("seo_page.html", services=services, lang=lang)
            return view
        app.add_url_rule(route, f"{lang}_page{idx + 1}", make_view())

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

    # Извлекаем информацию о видео
    video_title = response.get('title', 'Видео')
    thumbnail = response.get('thumbnail', '')
    author = response.get('author', 'Неизвестен')
    medias = response.get('medias', [])

    # Отображаем результат с кнопкой для скачивания
    return render_template('result.html', video_url=video_url, title=video_title, thumbnail=thumbnail, author=author, medias=medias)

if __name__ == '__main__':
    app.run(debug=True)
