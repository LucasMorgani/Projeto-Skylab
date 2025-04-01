from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "Empresa",
    "user": "docker",
    "password": "docker",
    "host": "database",  # Nome do serviço no docker-compose
    "port": "5432"
}

def get_funcionarios():
    """Recupera os funcionários do banco de dados."""
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

@app.route("/")
def homepage():
    funcionarios = get_funcionarios()
    return render_template("homepage.html", funcionarios=funcionarios)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")