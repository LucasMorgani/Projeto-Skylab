from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "Empresa",
    "user": "docker",
    "password": "docker",
    "host": "database",
    "port": "5432"
}

def get_db_connection():
    """Estabelece conexão com o banco de dados."""
    return psycopg2.connect(**DB_CONFIG)

def get_funcionarios(ordem='az', busca='', coluna_busca='nome'):
    """Recupera funcionários com filtros e ordenação."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Colunas válidas para busca
        colunas_validas = {
            'id': 'f.id',
            'nome': 'f.nome',
            'cargo': 'c.nome',
            'departamento': 'd.nome'
        }

        # Verifica se a coluna de busca é válida
        coluna = colunas_validas.get(coluna_busca, 'f.nome')

        # Query base
        query = sql.SQL("""
            SELECT f.id, f.nome, c.nome AS cargo, d.nome AS departamento
            FROM Funcionario f
            JOIN Cargo c ON f.cargo_id = c.id
            JOIN Departamento d ON f.departamento_id = d.id
        """)

        params = []
        
        # Adiciona filtro de busca se necessário
        if busca:
            query = sql.SQL("{query} WHERE {coluna} ILIKE %s").format(
                query=query,
                coluna=sql.SQL(coluna)
            )
            params.append(f"%{busca}%")

        # Mapeamento de ordenação
        ordem_map = {
            'az': sql.SQL("f.nome ASC"),
            'za': sql.SQL("f.nome DESC"),
            'id-up': sql.SQL("f.id ASC"),
            'id-down': sql.SQL("f.id DESC"),
            'cargo': sql.SQL("c.nome ASC"),
            'departamento': sql.SQL("d.nome ASC")
        }
        order_clause = ordem_map.get(ordem, sql.SQL("f.nome ASC"))

        # Adiciona ordenação
        query = sql.SQL("{query} ORDER BY {order}").format(
            query=query,
            order=order_clause
        )

        # Executa a query
        cur.execute(query, params)
        return cur.fetchall()

    except Exception as e:
        print(f"Erro ao buscar funcionários: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_cargos():
    """Recupera todos os cargos disponíveis."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM Cargo ORDER BY nome")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar cargos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_departamentos():
    """Recupera todos os departamentos disponíveis."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome FROM Departamento ORDER BY nome")
        return cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar departamentos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def adicionar_funcionario(nome, cargo_id, departamento_id):
    """Adiciona um novo funcionário ao banco de dados."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Funcionario (nome, cargo_id, departamento_id) VALUES (%s, %s, %s)",
            (nome, cargo_id, departamento_id)
        )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao adicionar funcionário: {e}")
        return False
    finally:
        if conn:
            conn.close()

@app.route("/")
def homepage():
    """Rota principal com suporte a filtros e busca."""
    try:
        # Obtém parâmetros da URL
        ordem = request.args.get('ordem', 'az')
        busca = request.args.get('busca', '')
        coluna_busca = request.args.get('coluna', 'nome')

        funcionarios = get_funcionarios(ordem, busca, coluna_busca)
        
        return render_template(
            "homepage.html",
            funcionarios=funcionarios,
            ordem_atual=ordem,
            busca_atual=busca,
            coluna_atual=coluna_busca,
            error=request.args.get('error')
        )
    except Exception as e:
        print(f"Erro na página principal: {e}")
        return render_template(
            "homepage.html",
            funcionarios=[],
            ordem_atual='az',
            busca_atual='',
            coluna_atual='nome',
            error=str(e)
        )

@app.route("/adicionar_funcionario", methods=["GET", "POST"])
def adicionar_funcionario_route():
    """Rota para adicionar novo funcionário."""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cargo_id = request.form.get("cargo", "")
        departamento_id = request.form.get("departamento", "")
        
        if not nome or not cargo_id or not departamento_id:
            return render_template(
                "adicionar_funcionario.html",
                cargos=get_cargos(),
                departamentos=get_departamentos(),
                error="Preencha todos os campos!"
            )
        
        if adicionar_funcionario(nome, cargo_id, departamento_id):
            return redirect(url_for("homepage"))
        else:
            return render_template(
                "adicionar_funcionario.html",
                cargos=get_cargos(),
                departamentos=get_departamentos(),
                error="Erro ao adicionar funcionário!"
            )
    
    # Se método GET, mostra o formulário
    return render_template(
        "adicionar_funcionario.html",
        cargos=get_cargos(),
        departamentos=get_departamentos()
    )

@app.route("/excluir_funcionarios", methods=["POST"])
def excluir_funcionarios():
    """Exclui funcionários selecionados e reordena os IDs restantes."""
    funcionarios_ids = request.form.getlist("funcionarios_ids")
    
    if not funcionarios_ids:
        return redirect(url_for("homepage"))
    
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Converte strings para inteiros
        ids = [int(id) for id in funcionarios_ids if id.isdigit()]
        
        if not ids:
            return redirect(url_for("homepage"))
        
        # Inicia transação
        conn.autocommit = False
        
        # 1. Exclui os funcionários selecionados
        placeholders = ','.join(['%s'] * len(ids))
        cur.execute(
            f"DELETE FROM Funcionario WHERE id IN ({placeholders})",
            ids
        )
        
        # 2. Obtém todos os IDs restantes ordenados
        cur.execute("SELECT id FROM Funcionario ORDER BY id")
        remaining_ids = [row[0] for row in cur.fetchall()]
        
        # 3. Reordena os IDs sequencialmente
        for new_id, old_id in enumerate(remaining_ids, start=1):
            if new_id != old_id:
                # Atualiza o ID mantendo as referências
                cur.execute(
                    "UPDATE Funcionario SET id = %s WHERE id = %s",
                    (new_id, old_id)
                )
        
        # 4. Atualiza a sequência SERIAL
        cur.execute(
            "SELECT setval('funcionario_id_seq', COALESCE((SELECT MAX(id) FROM Funcionario), 1))"
        )
        
        conn.commit()
        return redirect(url_for("homepage"))
    
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao excluir e reordenar funcionários: {e}")
        return redirect(url_for("homepage", error="Erro ao excluir funcionários"))
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")