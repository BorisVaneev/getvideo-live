import http.client
import json
from flask import Flask, render_template, request

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# 35 сервисов, делим их на 5 страниц по 7 сервисов на каждой
services_per_page = [
    ["instagram", "tiktok", "douyin", "capcut", "threads", "facebook", "kuaishou"],
    ["espn", "pinterest", "imgur", "ifunny", "reddit", "youtube", "twitter"],
    ["vimeo", "snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr"],
    ["febspot", "9gag", "rumble", "ted", "sohutv", "xiaohongshu", "ixigua"],
    ["meipai", "bluesky", "soundcloud", "mixcloud", "spotify", "zingmp3", "bandcamp"]
]

# языковые маршруты
languages = ['ru', 'en', 'es', 'zh']

# Создаем SEO-страницы для каждой страницы с сервисами на всех языках
for lang in languages:
    for i, services in enumerate(services_per_page):
        route = f"/{lang}/page{i+1}"
        def make_view(services=services, lang=lang):
            def view():
                return render_template("seo_page.html", services=services, lang=lang)
            return view
        app.add_url_rule(route, f"{lang}_page{i+1}", make_view())

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    if not video_url:
        return render_template("index.html", error="URL не указан")

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
    response = json.loads(data.decode("utf-8"))

    if 'medias' in response:
        download_url = response['medias']
        video_title = response['title']
        thumbnail = response.get('thumbnail', '')
        author = response.get('author', 'Неизвестен')
        return render_template("result.html", download_url=download_url, video_title=video_title, thumbnail=thumbnail, author=author)
    else:
        return render_template("result.html", error="Не удалось получить ссылку для скачивания.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
