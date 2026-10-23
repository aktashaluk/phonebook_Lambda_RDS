from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lambda Function URL adresinizi buraya yazın
LAMBDA_URL = "https://YOUR_LAMBDA_FUNCTION_URL.lambda-url.region.on.aws/"

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    records = []
    error_message = None

    try:
        # Lambda'dan kayıtları çekme (GET isteği)
        response = requests.get(f"{LAMBDA_URL}?search={search_query}")
        if response.status_code == 200:
            records = response.json().get('data', [])
        else:
            error_message = "Kayıtlar getirilemedi."
    except Exception as e:
        error_message = f"Bağlantı hatası: {str(e)}"

    return render_template('index.html', records=records, search_query=search_query, error_message=error_message)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')

    try:
        # Lambda'ya kayıt gönderme (POST isteği)
        payload = {"name": name, "phone_number": phone_number}
        requests.post(LAMBDA_URL, json=payload)
    except Exception as e:
        print("Ekleme hatası:", e)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)