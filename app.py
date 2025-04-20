from flask import Flask, render_template, request
import http.client
import json
import os

app = Flask(__name__)

# Ваш RapidAPI‑ключ и хост
RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# Разбиваем 35 сервисов на 5 SEO‑страниц по 7 штук
pages = {
    "instagram-tiktok-douyin-capcut-threads-facebook-kuaishou": [
        "Instagram", "TikTok", "Douyin", "Capcut", "Threads", "Facebook", "Kuaishou"
    ],
    "espn-pinterest-imgur-ifunny-reddit-youtube-twitter": [
        "Espn", "Pinterest", "Imgur", "Ifunny", "Reddit", "YouTube", "Twitter"
    ],
    "vimeo-snapchat-dailymotion-sharechat-likee-linkedin-tumblr": [
        "Vimeo", "Snapchat", "Dailymotion", "Sharechat", "Likee", "LinkedIn", "Tumblr"
    ],
    "febspot-9gag-rumble-ted-sohutv-xiaohongshu-ixigua": [
        "Febspot", "9GAG", "Rumble", "Ted", "SohuTv", "Xiaohongshu", "Ixigua"
    ],
    "meipai-bluesky-soundcloud-mixcloud-spotify-zingmp3-bandcamp": [
        "Meipai", "Bluesky", "Soundcloud", "Mixcloud", "Spotify", "Zingmp3", "Bandcamp"
    ]
}

# Языковые префиксы
languages = ["ru", "en", "es", "zh"]

@app.route('/')
def index():
    return render_template("base.html")

# Динамически регистрируем 5×4 = 20 маршрутов
for lang in languages:
    for slug, services in pages.items():
        route = f"/{lang}/{slug}"
        endpoint = f"{lang}_{slug}"
        def make_view(slist=services, l=lang, slug=slug):
            def view():
                # Передаём в шаблон: список названий сервисов, язык и slug
                return render_template(
                    "seo_page.html",
                    services=slist,
                    lang=l,
                    slug=slug
                )
            return view
        app.add_url_rule(route, endpoint, make_view())

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
    return data, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # Используем порт из окружения (Render/Hetzner) или 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
