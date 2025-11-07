# app.py
from flask import Flask, request, redirect, session, send_from_directory, url_for, abort, make_response
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
# ZAMIEN: ustaw bezpieczny, losowy secret key przed uruchomieniem w środowisku produkcyjnym
app.secret_key = "replace_this_with_a_random_secret_key_please_change"

# POPRAWNE dane logowania (tylko po stronie serwera)
VALID_USERNAME = "secure_user"
VALID_PASSWORD = "secure_pass123"

LOGIN_PAGE_FILENAME = "index.html"

@app.route("/")
def index():
    # Zwracamy zawartość pliku index.html bez modyfikowania go
    if not os.path.exists(INDEX_FILENAME):
        return "Brak pliku index.html", 500
    with open(INDEX_FILENAME, 'r', encoding='utf-8') as f:
        html = f.read()
    # Zwracamy surowy HTML - on zawiera logikę klienta tylko do wysyłki POST na /login
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Serwerowa weryfikacja
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Poprawne dane -> ustaw sesję i przekieruj do /secret
        session['logged_in'] = True
        session['user'] = username
        return redirect(url_for('secret'))
    else:
        # Niepoprawne -> przekieruj z parametrem error=1
        return redirect(url_for('index') + "?error=1")

@app.route("/secret")
def secret():
    # Dostęp tylko dla zalogowanych (sprawdzamy sesję)
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    # Serwerowa flaga (widoczna tylko po poprawnym loginie)
    server_flag = "CTF{server_side_secret_2026}"
    user = session.get('user', '')
    # Generujemy prostą stronę z flagą (nie zapisujemy jej w plikach statycznych)
    html = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SecureBank - Sekret</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="login-container">
    <h1>Dostęp przyznany</h1>
    <p>Witaj, {user}. Pomyślnie zalogowano do ukrytej sekcji.</p>
    <div class="flag-box">
      <h2>Twoja flaga CTF (serwerowa):</h2>
      <pre style="font-size:18px; font-weight:600;">{server_flag}</pre>
    </div>
    <p><a href="{url_for('logout')}">Wyloguj</a></p>
  </div>
</body>
</html>"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

# Pozostawiamy serwowanie plików statycznych Flaskowi (folder static)
# Uruchomienie serwera:
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
