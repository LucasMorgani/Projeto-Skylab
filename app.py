from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/teste")
def users():
    return "TELA DE CRIAÇÃO DE USUARIO"

if __name__ == "__main__":
    app.run(debug=True)