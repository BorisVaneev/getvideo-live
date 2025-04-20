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
    
    # Печатаем полученный URL для отладки
    print(f"Получен URL: {video_url}")

    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    payload = json.dumps({"url": video_url})
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': 'application/json'
    }
    
    try:
        conn.request("POST", "/v1/social/autolink", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Декодируем данные и выводим их для отладки
        response_data = data.decode("utf-8")
        print(f"Ответ от API: {response_data}")

        # Пытаемся получить ссылку на скачивание
        response_json = json.loads(response_data)
        if 'medias' in response_json and len(response_json['medias']) > 0:
            video_url = response_json['medias'][0]['url']
            video_title = response_json.get('title', 'video')
            video_author = response_json.get('author', 'Unknown')
            video_thumbnail = response_json.get('thumbnail', '')
            
            # Отправляем данные на шаблон
            return render_template("result.html", 
                                   video_url=video_url, 
                                   video_title=video_title, 
                                   video_author=video_author, 
                                   video_thumbnail=video_thumbnail)
        else:
            # Если ссылки для скачивания нет, возвращаем ошибку
            return render_template("result.html", error="Не удалось получить ссылку для скачивания.")
    except Exception as e:
        # Если произошла ошибка при запросе, выводим её
        print(f"Ошибка при запросе: {e}")
        return render_template("result.html", error="Произошла ошибка при обработке запроса.")

if __name__ == '__main__':
    app.run(debug=True)
