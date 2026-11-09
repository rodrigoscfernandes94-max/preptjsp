import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_PATH = "tjsp_estudos.db"

def garantir_banco():
    """Garante que o banco e a tabela existam e tenham dados"""
    try:
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia TEXT,
                enunciado TEXT,
                alternativa_a TEXT,
                alternativa_b TEXT,
                alternativa_c TEXT,
                alternativa_d TEXT,
                alternativa_e TEXT,
                gabarito TEXT,
                comentario TEXT
            )
        """)
        conexao.commit()
        
        cursor.execute("SELECT COUNT(*) FROM questoes")
        if cursor.fetchone()[0] == 0:
            questoes_iniciais = [
                (
                    "Língua Portuguesa",
                    "Embora o oficial tivesse recebido a ordem com antecedência, somente a cumpriu após nova determinação. A palavra “Embora” estabelece relação de:",
                    "causa.", "conclusão.", "concessão.", "condição.", "finalidade.",
                    "C", "A conjunção 'embora' introduz oração subordinada adverbial concessiva."
                ),
                (
                    "Direito Processual Civil",
                    "A citação válida, no processo civil:",
                    "não produz qualquer efeito processual.",
                    "induz litispendência, torna litigiosa a coisa e constitui em mora o devedor, ressalvadas as hipóteses legais.",
                    "encerra automaticamente o processo.",
                    "impede qualquer acordo.",
                    "substitui a sentença.",
                    "B", "Conforme o art. 240 do CPC, a citação válida induz litispendência e constitui em mora o devedor."
                )
            ]
            cursor.executemany("""
                INSERT INTO questoes (materia, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, gabarito, comentario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, questoes_iniciais)
            conexao.commit()
            
        conexao.close()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

# Executa ao iniciar
garantir_banco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    try:
        conexao = sqlite3.connect(DB_PATH)
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        rows = cursor.execute('SELECT * FROM questoes').fetchall()
        conexao.close()
        
        questoes = []
        for row in rows:
            questoes.append({
                "id": row["id"],
                "materia": row["materia"] if "materia" in row.keys() else "Geral",
                "enunciado": row["enunciado"],
                "alternativas": [
                    row["alternativa_a"],
                    row["alternativa_b"],
                    row["alternativa_c"],
                    row["alternativa_d"],
                    row["alternativa_e"]
                ],
                "correta": row["gabarito"],
                "comentario": row["comentario"]
            })
        return jsonify(questoes)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
