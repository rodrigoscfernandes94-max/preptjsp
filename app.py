import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def inicializar_banco():
    """Garante que a tabela e o banco de dados inicial padrão existam"""
    conexao = sqlite3.connect("tjsp_estudos.db")
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bloco TEXT,
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
    
    # Se o banco estiver vazio, insere algumas questões padrão da VUNESP para o TJSP
    cursor.execute("SELECT COUNT(*) FROM questoes")
    total = cursor.fetchone()[0]
    
    if total == 0:
        questoes_iniciais = [
            ("Bloco I", "Língua Portuguesa", "Embora o oficial tivesse recebido a ordem com antecedência, somente a cumpriu após nova determinação. A palavra “Embora” estabelece relação de:", "causa.", "conclusão.", "concessão.", "condição.", "finalidade.", "C", "A conjunção 'embora' introduz oração subordinada adverbial concessiva."),
            ("Bloco II", "Direito Processual Civil", "A citação válida, no processo civil:", "não produz qualquer efeito processual.", "induz litispendência, torna litigiosa a coisa e constitui em mora o devedor, ressalvadas as hipóteses legais.", "encerra automaticamente o processo.", "impede qualquer acordo.", "substitui a sentença.", "B", "Conforme o art. 240 do CPC, a citação válida induz litispendência e constitui em mora o devedor."),
            ("Bloco II", "Direito Constitucional", "São princípios expressamente relacionados à Administração Pública no art. 37 da Constituição Federal:", "legalidade, pessoalidade, sigilo, eficiência e supremacia.", "legalidade, impessoalidade, moralidade, publicidade e eficiência.", "moralidade, segredo, hierarquia, publicidade e eficiência.", "legalidade, informalidade, publicidade, pessoalidade e eficiência.", "apenas legalidade e eficiência.", "B", "Mnemônico LIMPE: Legalidade, Impessoalidade, Moralidade, Publicidade e Eficiência.")
        ]
        cursor.executemany("""
            INSERT INTO questoes (bloco, materia, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, gabarito, comentario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, questoes_iniciais)
        conexao.commit()
        
    conexao.close()

# Executa a inicialização do banco assim que o app sobe no Render
inicializar_banco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    conexao = sqlite3.connect('tjsp_estudos.db')
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    rows = cursor.execute('SELECT * FROM questoes').fetchall()
    conexao.close()
    
    questoes = []
    for row in rows:
        questoes.append({
            "id": row["id"],
            "materia": row["materia"],
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
