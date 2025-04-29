
from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def salvar_adotante(dados):
    conn = sqlite3.connect('adotantes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO adotantes (nome, cpf, telefone, email, endereco, nome_animal, especie, microchip, data, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (dados['nome'], dados['cpf'], dados['telefone'], dados['email'], dados['endereco'],
                    dados['nome_animal'], dados['especie'], dados['microchip'], dados['data'], dados['observacoes']))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dados = {chave: request.form.get(chave, '') for chave in ['nome', 'cpf', 'telefone', 'email', 'endereco', 'nome_animal', 'especie', 'microchip', 'data', 'observacoes']}
        salvar_adotante(dados)
        return redirect(url_for('index'))
    return render_template('cadastro_adotante.html')

@app.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    resultados = []
    especie_contagem = {}
    grafico_path = None
    if request.method == 'POST':
        inicio = request.form['data_inicio']
        fim = request.form['data_fim']
        conn = sqlite3.connect('adotantes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, nome_animal, especie, microchip, data FROM adotantes WHERE data BETWEEN ? AND ?", (inicio, fim))
        resultados = cursor.fetchall()

        cursor.execute("SELECT especie, COUNT(*) FROM adotantes WHERE data BETWEEN ? AND ? GROUP BY especie", (inicio, fim))
        especie_contagem = dict(cursor.fetchall())
        conn.close()

        # Gerar gráfico
        if especie_contagem:
            especies = list(especie_contagem.keys())
            quantidades = list(especie_contagem.values())
            plt.figure(figsize=(8, 5))
            plt.bar(especies, quantidades)
            plt.xlabel("Espécie")
            plt.ylabel("Quantidade")
            plt.title("Adoções por Espécie")
            plt.tight_layout()
            grafico_path = os.path.join("static/graficos", "grafico_especies.png")
            plt.savefig(grafico_path)
            plt.close()

    return render_template('relatorios.html', resultados=resultados, especie_contagem=especie_contagem, grafico=grafico_path)
from flask import render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
import sqlite3

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('adotantes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT senha, tipo FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and check_password_hash(usuario[0], senha):
            session['email'] = email
            session['tipo'] = usuario[1]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro="Usuário ou senha inválidos.")
    
    return render_template('login.html')
