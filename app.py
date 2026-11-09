import os
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tjsp_estudos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM questoes').fetchall()
    conn.close()
    
    questoes = []
    for row in rows:
        questoes.append({
            "id": row["id"],
            "materia": row["materia"],
            "tema": row["tema"],
            "enunciado": row["enunciado"],
            "alternativas": [
                row["alternativa_a"],
                row["alternativa_b"],
                row["alternativa_c"],
                row["alternativa_d"],
                row["alternativa_e"]
            ],
            "correta": row["correta"],
            "comentario": row["comentario"]
        })
    return jsonify(questoes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
