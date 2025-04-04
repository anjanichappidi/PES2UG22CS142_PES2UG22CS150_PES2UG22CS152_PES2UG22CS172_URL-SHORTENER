from flask import Flask, request, redirect, render_template
import redis
import random
import string
import os

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_password = os.environ.get("REDIS_PASSWORD", "mypassword")

client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()
        client.set(short_url, original_url)
        return render_template('index.html', short_url=request.host_url + short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    original_url = client.get(short_url)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
