from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Твои ключи от Supabase
SUPABASE_URL = "https://atvvfkqtdbllrttzcyn.supabase.co"
SUPABASE_KEY = "sb_publishable_3fpcwkRGD84VX-m0hEIi9Q_iiQ1nZ83"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@app.route('/')
def home():
    return "Сервер мессенджера работает!"

# --- РЕГИСТРАЦИЯ ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    display_name = data.get('display_name')

    # 1. Проверяем белый список
    check_url = f"{SUPABASE_URL}/rest/v1/allowed_users?username=eq.{username}"
    res = requests.get(check_url, headers=HEADERS)
    if not res.json():
        return jsonify({"error": "Вас нет в белом списке!"}), 403

    # 2. Создаем пользователя
    insert_url = f"{SUPABASE_URL}/rest/v1/users"
    user_data = {"username": username, "password_hash": password, "display_name": display_name}
    res = requests.post(insert_url, headers=HEADERS, json=user_data)
    
    if res.status_code == 201:
        return jsonify({"message": "Успешная регистрация!"}), 201
    return jsonify({"error": "Ошибка регистрации"}), 400

# --- ВХОД ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&password_hash=eq.{password}"
    res = requests.get(url, headers=HEADERS)
    
    if res.json():
        return jsonify({"message": "Успешный вход!"}), 200
    return jsonify({"error": "Неверный логин или пароль"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
