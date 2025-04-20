from flask import Flask, render_template, request
import http.client
import json
from datetime import datetime

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# SEO-группы (5 штук)
groups = {
    "group1": ["Instagram", "Tiktok", "Douyin", "Capcut", "Threa.ds"],
    "group2": ["Facebook", "Kuaishou", "Espn", "Pinterest", "imgur"],
    "group3": ["ifunny", "Reddit", "Youtube", "Twitter", "Vimeo"],
    "group4": ["Snapchat", "Dailymotion", "Sharechat", "Likee", "Linkedin"],
    "group5": ["Tumblr", "Febspot", "9GAG", "Rumble", "Ted", "SohuTv", "Xiaohongshu", "Ixigua", "Meipai", "Bluesky", "Soundcloud", "Mixcloud", "Spotify", "Zingmp3", "Bandcamp"]
}

languages = ["ru", "en", "es", "zh"]

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    links = []
    for lang in languages:
        for i, group in enumerate(groups.keys(), 1):
            links.append({
                "lang": lang,
                "group": f"группа {i}" if lang == "ru" else f"group {i}",
                "url": f"/{lang}/group{i}"
            })
    return render_template("index.html", links=links)

# SEO-страницы
for lang in languages:
    for i, (group_key, services) in enumerate(groups.items(), 1):
        route = f"/{lang}/group{i}"
        def make_view(s=services, l=lang, g=i):
            def view():
                return render_template("seo_page.html", services=s, lang=l, group_number=g)
            return view
        app.add_url_rule(route, f"{lang}_group{i}", make_view())

# Загрузка видео
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

    try:
        result = json.loads(data.decode("utf-8"))
        return render_template("result.html", result=result)
    except:
        return f"Ошибка: {data.decode('utf-8')}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
