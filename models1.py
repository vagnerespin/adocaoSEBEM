
import sqlite3

def buscar_adocoes_por_periodo(inicio, fim):
    conn = sqlite3.connect("adotantes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nome_animal, data FROM adotantes WHERE data BETWEEN ? AND ?", (inicio, fim))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
