import os
import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect("tjsp_estudos.db")
    cursor = conexao.cursor()

    # Cria a tabela de questões se ela não existir
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
    conexao.commit()
    conexao.close()
    print("Banco de dados verificado/criado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()
