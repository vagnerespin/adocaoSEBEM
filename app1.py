
from flask import Flask, render_template, request
import sqlite3
import matplotlib.pyplot as plt
import os
from models import buscar_adocoes_por_periodo

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    if request.method == "POST":
        inicio = request.form.get("inicio")
        fim = request.form.get("fim")
        dados = buscar_adocoes_por_periodo(inicio, fim)

        nomes = [d[1] for d in dados]
        contagem = {}
        for nome in nomes:
            contagem[nome] = contagem.get(nome, 0) + 1

        especies = list(contagem.keys())
        valores = list(contagem.values())

        plt.figure(figsize=(8,4))
        plt.bar(especies, valores)
        plt.title("Animais Adotados")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if not os.path.exists("static/graficos"):
            os.makedirs("static/graficos")
        plt.savefig("static/graficos/grafico.png")
        plt.close()

        return render_template("relatorios.html", dados=dados, grafico="static/graficos/grafico.png")
    return render_template("relatorios.html", dados=None, grafico=None)

if __name__ == "__main__":
    app.run(debug=True)
