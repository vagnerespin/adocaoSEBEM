
from flask import Flask, render_template, request, redirect, flash
import sqlite3
import matplotlib.pyplot as plt
import os
from models import buscar_adocoes_por_periodo

app = Flask(__name__)
app.secret_key = 'segredo'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]
        nome_animal = request.form["nome_animal"]
        especie = request.form["especie"]
        microchip = request.form["microchip"]
        data = request.form["data"]
        observacoes = request.form["observacoes"]

        conn = sqlite3.connect("adotantes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO adotantes (nome, cpf, telefone, email, endereco, nome_animal, especie, microchip, data, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (nome, cpf, telefone, email, endereco, nome_animal, especie, microchip, data, observacoes))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("cadastro.html")

@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    if request.method == "POST":
        inicio = request.form.get("inicio")
        fim = request.form.get("fim")
        dados = buscar_adocoes_por_periodo(inicio, fim)

        if not dados:
            flash("Nenhum dado encontrado no período selecionado.")
            return render_template("relatorios.html", dados=None, grafico=None)

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
