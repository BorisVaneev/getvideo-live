import http.client
import json
from flask import Flask, render_template, request

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
        download_url = response['medias'][0]['url']
        video_title = response['title']
        thumbnail = response.get('thumbnail', '')
        author = response.get('author', 'Неизвестен')
        return render_template("result.html", download_url=download_url, video_title=video_title, thumbnail=thumbnail, author=author)
    else:
        return render_template("result.html", error="Не удалось получить ссылку для скачивания.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
