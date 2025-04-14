# app.py
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "Empresa",
    "user": "docker",
    "password": "docker",
    "host": "database",
    "port": "5432"
}

def get_funcionarios():
    """Recupera todos os funcionários do banco de dados com seus cargos e departamentos."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT f.id, f.nome, c.nome AS cargo, d.nome AS departamento
        FROM Funcionario f
        JOIN Cargo c ON f.cargo_id = c.id
        JOIN Departamento d ON f.departamento_id = d.id
    """)
    
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
    return funcionarios

def get_cargos():
    """Recupera todos os cargos disponíveis no banco de dados."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM Cargo")
    cargos = cur.fetchall()
    cur.close()
    conn.close()
    return cargos

def get_departamentos():
    """Recupera todos os departamentos disponíveis no banco de dados."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM Departamento")
    departamentos = cur.fetchall()
    cur.close()
    conn.close()
    return departamentos

def adicionar_funcionario(nome, cargo_id, departamento_id):
    """Adiciona um novo funcionário ao banco de dados."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Funcionario (nome, cargo_id, departamento_id) VALUES (%s, %s, %s)",
            (nome, cargo_id, departamento_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao adicionar funcionário: {e}")
        return False
    finally:
        cur.close()
        conn.close()

@app.route("/")
def homepage():
    """Rota principal que exibe a lista de funcionários."""
    funcionarios = get_funcionarios()
    return render_template("homepage.html", funcionarios=funcionarios)

@app.route("/adicionar_funcionario", methods=["GET", "POST"])
def adicionar_funcionario_route():
    """Rota para adicionar novo funcionário (exibe formulário e processa submissão)."""
    if request.method == "POST":
        nome = request.form["nome"]
        cargo_id = request.form["cargo"]
        departamento_id = request.form["departamento"]
        
        if adicionar_funcionario(nome, cargo_id, departamento_id):
            return redirect(url_for("homepage"))
        else:
            return "Erro ao adicionar funcionário", 400
    
    # Se método GET, mostra o formulário
    cargos = get_cargos()
    departamentos = get_departamentos()
    return render_template(
        "adicionar_funcionario.html",
        cargos=cargos,
        departamentos=departamentos
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")