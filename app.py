from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello, Flask!"

@app.route("/teste")
def users():
    return "TELA DE CRIAÇÃO DE USUARIO"

if __name__ == "__main__":
    app.run(debug=True)
    