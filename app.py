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

    if res.status != 200:
        return f"Ошибка при получении данных: {data.decode('utf-8')}", 400

    try:
        video_data = json.loads(data)
        video_url = video_data.get("medias")[0].get("url", "")
        video_title = video_data.get("title", "video")
        video_thumbnail = video_data.get("thumbnail", "")
        video_medias = video_data.get("medias", [])

        if not video_url:
            return "Не удалось получить ссылку для скачивания.", 400

        return render_template("result.html", 
                               video_url=video_url, 
                               video_title=video_title, 
                               video_thumbnail=video_thumbnail,
                               video_medias=video_medias)
    except Exception as e:
        return f"Ошибка при обработке данных: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
