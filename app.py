from flask import Flask, render_template, request, Response, redirect, url_for
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

# Динамически создаем страницы для каждого языка и группы сервисов
for lang, pages in SERVICES.items():
    for page, services in pages.items():
        route = f"/{lang}/{page}"
        def make_view(p=page, s=services, l=lang):
            def view():
                return render_template("seo_page.html", services=s, lang=l, page=p)
            return view
        app.add_url_rule(route, f"{lang}_{page}", make_view())

# Обработка формы — получение ссылки, запрос к RapidAPI и отображение кнопки скачивания
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return "URL не указан", 400

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"url": video_url})
    response = requests.post(f"https://{RAPIDAPI_HOST}/v1/social/autolink", headers=headers, data=payload)

    try:
        result = response.json()
        return render_template("result.html", result=result)
    except Exception as e:
        return f"Ошибка обработки данных: {e}"

# Обработка скачивания по прямой ссылке
@app.route('/download_video')
def download_video():
    direct_url = request.args.get('url')
    if not direct_url:
        return "No download URL provided", 400

    response = requests.get(direct_url, stream=True)
    if response.status_code == 200:
        return Response(
            response.iter_content(chunk_size=1024),
            headers={
                'Content-Disposition': 'attachment; filename="video.mp4"',
                'Content-Type': 'video/mp4',
            }
        )
    return "Error: Could not fetch video", 400

if __name__ == '__main__':
    app.run(debug=True)
