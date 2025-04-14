from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Chave via environment

# Configuração segura do DB
DB_CONFIG = {
    "dbname": os.getenv('DB_NAME', 'Empresa'),
    "user": os.getenv('DB_USER', 'docker'),
    "password": os.getenv('DB_PASSWORD', 'docker'),
    "host": os.getenv('DB_HOST', 'database'),
    "port": os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=psycopg2.extras.DictCursor)

# Middlewares atualizados
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            flash('Acesso não autorizado', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
                user = cur.fetchone()

                if user and check_password_hash(user['password'], password):
                    if user['ativo']:
                        session['user'] = user['username']
                        session['admin'] = user['admin']
                        return redirect(url_for('homepage'))
                    flash('Conta desativada', 'error')
                else:
                    flash('Credenciais inválidas', 'error')
        except Exception as e:
            flash('Erro no sistema', 'error')
            app.logger.error(f"Login error: {e}")
        finally:
            conn.close()

    return render_template('homepage.html')

# ... (outras rotas mantendo a mesma estrutura segura)