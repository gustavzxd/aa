from flask import Flask, request, session, redirect, jsonify, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para sessão

# Dados em memória
occurrences = []  # Lista de ocorrências
next_id = 1       # Próximo ID
logs = []         # Logs de eventos

def add_log(user, action):
    """Adiciona entrada no log com data, hora, usuário e ação."""
    now = datetime.now()
    logs.append({
        'data': now.strftime("%Y-%m-%d"),
        'hora': now.strftime("%H:%M:%S"),
        'usuario': user,
        'acao': action
    })

@app.after_request
def set_secure_headers(response):
    """Define cabeçalhos de segurança (CSP, X-Frame-Options, etc.)."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    csp = "default-src 'self' https://unpkg.com https://tile.openstreetmap.org; "
    csp += "style-src 'self' https://unpkg.com; "
    csp += "script-src 'self' https://unpkg.com; "
    csp += "img-src 'self' data: https://tile.openstreetmap.org; "
    csp += "font-src 'self';"
    response.headers['Content-Security-Policy'] = csp
    return response

@app.route('/favicon.ico')
def favicon():
    return ('', 204)  # Sem favicon

# Rota pública: página de login
@app.route('/login', methods=['GET'])
def login_page():
    if session.get('user'):
        return redirect('/index')
    return send_from_directory('pages', 'login.html')

# Ação de login (POST JSON {username, password})
# No arquivo server.py, altere a rota de login:

@app.route('/login', methods=['POST'])
def login_action():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if username == 'gustavo' and password == 'gotoso':
        session['user'] = username
        add_log(username, 'Login')
        return jsonify({'ok': True})
    else:
        # Retornamos ok: False explicitamente para o JS tratar no segundo .then
        return jsonify({'ok': False}), 401

# Logout
@app.route('/logout')
def logout():
    user = session.get('user')
    session.clear()
    if user:
        add_log(user, 'Logout')
    return redirect('/login')

# Decorator para rotas protegidas
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user'):
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

# Rotas protegidas que servem HTML estáticos
@app.route('/')
@login_required
def root():
    return send_from_directory('pages', 'index.html')

@app.route('/index')
@login_required
def index_page():
    return send_from_directory('pages', 'index.html')

@app.route('/lista')
@login_required
def lista_page():
    return send_from_directory('pages', 'lista.html')

@app.route('/mapa')
@login_required
def mapa_page():
    return send_from_directory('pages', 'mapa.html')

@app.route('/logs')
@login_required
def logs_page():
    return send_from_directory('pages', 'logs.html')

# API: retorna todas ocorrências em JSON
@app.route('/ocorrencias', methods=['GET'])
def get_ocorrencias():
    if not session.get('user'):
        return jsonify({'error': 'Não autorizado'}), 403
    return jsonify(occurrences)

# API: registra nova ocorrência (JSON esperado: tipo, prioridade, descricao, endereco, lat, lon)
@app.route('/registrar_ocorrencia', methods=['POST'])
def registrar_ocorrencia():
    if not session.get('user'):
        return jsonify({'error': 'Não autorizado'}), 403
    global next_id
    data = request.get_json() or {}
    entry = {
        'id': next_id,
        'data': datetime.now().strftime("%Y-%m-%d"),
        'hora': datetime.now().strftime("%H:%M:%S"),
        'tipo': data.get('tipo', ''),
        'prioridade': data.get('prioridade', ''),
        'descricao': data.get('descricao', ''),
        'endereco': data.get('endereco', ''),
        'lat': data.get('lat'),
        'lon': data.get('lon')
    }
    occurrences.append(entry)
    add_log(session['user'], f'Criou ocorrência {next_id}')
    next_id += 1
    return jsonify({'ok': True})

# API: exclui ocorrência por ID (JSON {id})
@app.route('/excluir_ocorrencia', methods=['POST'])
def excluir_ocorrencia():
    if not session.get('user'):
        return jsonify({'error': 'Não autorizado'}), 403
    data = request.get_json() or {}
    occ_id = data.get('id')
    if occ_id is None:
        return jsonify({'ok': False}), 400
    for occ in occurrences:
        if occ['id'] == occ_id:
            occurrences.remove(occ)
            add_log(session['user'], f'Excluiu ocorrência {occ_id}')
            return jsonify({'ok': True})
    return jsonify({'ok': False}), 404

# API: retorna logs em JSON
@app.route('/logs_data', methods=['GET'])
def get_logs():
    if not session.get('user'):
        return jsonify({'error': 'Não autorizado'}), 403
    return jsonify(logs)

if __name__ == '__main__':
    # Garante existência das pastas
    os.makedirs('pages', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=False)