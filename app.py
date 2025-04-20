from flask import Flask, render_template, request, Response, send_file
import yt_dlp
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
@app.route('/download_video', methods=['GET'])
def download_video():
    # Получаем ссылку на видео из параметра запроса
    video_url = request.args.get('url')
    
    # Проверяем, с какого источника видео
    if "youtube.com" in video_url or "youtu.be" in video_url:
        # Используем yt-dlp для загрузки видео с YouTube
        return download_from_youtube(video_url)
    elif "instagram.com" in video_url:
        # Используем yt-dlp для загрузки видео с Instagram
        return download_from_instagram(video_url)
    else:
        # Для других источников
        return download_from_other_sources(video_url)

def download_from_youtube(video_url):
    # Используем yt-dlp для получения ссылки на видео с YouTube
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'temp_video.mp4',  # Временно сохраняем видео на сервере
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_file = 'temp_video.mp4'  # Путь к сохраненному файлу
    
    # Отправляем видеофайл
    return send_file(video_file, as_attachment=True, download_name="video.mp4")

def download_from_instagram(video_url):
    # Используем yt-dlp для получения ссылки на видео с Instagram
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'temp_video_instagram.mp4',  # Временно сохраняем видео на сервере
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_file = 'temp_video_instagram.mp4'  # Путь к сохраненному файлу
    
    # Отправляем видеофайл
    return send_file(video_file, as_attachment=True, download_name="instagram_video.mp4")

def download_from_other_sources(video_url):
    # Для других источников, используем requests для загрузки видео
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
