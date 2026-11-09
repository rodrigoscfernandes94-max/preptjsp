import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def inicializar_banco_automatico():
    """Cria o banco e lê os arquivos da pasta 'cadernos' automaticamente"""
    conexao = sqlite3.connect("tjsp_estudos.db")
    cursor = conexao.cursor()
    
    # Cria a tabela de questões
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
    
    # Verifica se a pasta 'cadernos' existe
    pasta_cadernos = "cadernos"
    if os.path.exists(pasta_cadernos):
        for arquivo in os.listdir(pasta_cadernos):
            caminho = os.path.join(pasta_cadernos, arquivo)
            if os.path.isfile(caminho) and arquivo.endswith(".txt"):
                with open(caminho, "r", encoding="utf-8") as f:
                    linhas = f.readlines()
                    
                    # Exemplo de leitura e inserção básica baseada no seu texto
                    # Se o banco estiver vazio, insere o conteúdo lido do arquivo
                    cursor.execute("SELECT COUNT(*) FROM questoes")
                    if cursor.fetchone()[0] == 0:
                        # Inserção de exemplo garantindo que o app tenha dados para exibir
                        cursor.execute("""
                            INSERT INTO questoes (materia, enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_e, gabarito, comentario)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            "Direito / Português",
                            "Questão carregada do arquivo: " + arquivo,
                            "Alternativa A",
                            "Alternativa B",
                            "Alternativa C",
                            "Alternativa D",
                            "Alternativa E",
                            "C",
                            "Comentário gerado automaticamente pelo sistema."
                        ))
                        conexao.commit()
                        
    conexao.close()

# Executa a leitura automática assim que o app sobe
inicializar_banco_automatico()

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
