from flask import Flask, render_template, request, redirect, url_for, send_file, Response
import http.client
import json
import requests
import traceback  # Для логов ошибок

app = Flask(__name__)

RAPIDAPI_KEY = "aa3d356f13msh3974bc1b6659014p111df9jsn9a452dae36bc"
RAPIDAPI_HOST = "auto-download-all-in-one.p.rapidapi.com"

ALL_SERVICES = {
    "page1": ["instagram", "tiktok", "facebook", "twitter", "youtube", "reddit", "vimeo"],
    "page2": ["reddit", "linkedin", "pinterest", "tumblr", "vimeo", "soundcloud", "spotify"],
    "page3": ["soundcloud", "spotify", "mixcloud", "bandcamp", "zingmp3", "vimeo", "youtube"],
    "page4": ["douyin", "kuaishou", "xiaohongshu", "ixigua", "meipai", "twitter", "vimeo"],
    "page5": ["snapchat", "dailymotion", "sharechat", "likee", "linkedin", "tumblr", "9gag"]
}

SERVICES = {
    "ru": ALL_SERVICES,
    "en": ALL_SERVICES,
    "es": ALL_SERVICES,
    "zh": ALL_SERVICES
}

@app.route('/')
def index():
    print("🟢 Открыта главная страница /")
    return render_template("index.html")

# Динамически создаём страницы
for lang, pages in SERVICES.items():
    for page, services in pages.items():
        route = f"/{lang}/{page}"
        def make_view(p=page, s=services, l=lang):
            def view():
                print(f"🟢 Открыта страница: /{l}/{p} — сервисы: {s}")
                return render_template("seo_page.html", services=s, lang=l, page=p)
            return view
        app.add_url_rule(route, f"{lang}_{page}", make_view())

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    print(f"📥 Получен URL для загрузки: {video_url}")

    if not video_url:
        print("❌ URL не указан!")
        return "URL не указан", 400

    try:
        conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
        payload = json.dumps({"url": video_url})
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST,
            'Content-Type': 'application/json'
        }

        print("📡 Отправка запроса на RapidAPI...")
        conn.request("POST", "/v1/social/autolink", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(f"📨 Ответ от RapidAPI: {data[:500]}...")  # ограничим вывод

        result = json.loads(data)
        return render_template("result.html", result=result)

    except Exception as e:
        print("🔥 Ошибка при обработке запроса:")
        traceback.print_exc()
        return f"Ошибка обработки данных: {e}"

@app.route('/download_video', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    print(f"📥 Попытка скачать видео по URL: {video_url}")

    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            print("✅ Видео успешно загружено, отправляем пользователю")
            headers = {
                'Content-Disposition': 'attachment; filename="video.mp4"',
                'Content-Type': 'video/mp4',
            }
            return Response(response.iter_content(chunk_size=1024), headers=headers)

        print(f"❌ Не удалось получить видео. Код: {response.status_code}")
        return "Error: Could not fetch video", 400
    except Exception as e:
        print("🔥 Ошибка при скачивании видео:")
        traceback.print_exc()
        return f"Ошибка: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
