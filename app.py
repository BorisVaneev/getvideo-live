from flask import Flask, render_template, request
import http.client
import json

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

# языковые маршруты
routes = {
    "ru": ["instagram", "tiktok", "facebook", "twitter"],
    "en": ["youtube", "reddit", "linkedin", "pinterest"],
    "es": ["tumblr", "vimeo", "ted", "copied"],
    "zh": ["xiaohongshu", "ixigua", "douyin", "kuaishou"]
}

@app.route('/')
def index():
    return render_template("base.html")

# создаём SEO‑страницы динамически
for lang, services in routes.items():
    for service in services:
        route = f"/{lang}/{service}"
        def make_view(s=service, l=lang):
            def view():
                return render_template("seo_page.html", service=s, lang=l)
            return view
        app.add_url_rule(route, f"{lang}_{service}", make_view())

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
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
