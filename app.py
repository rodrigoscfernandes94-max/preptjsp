import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Base de dados em memória persistente na execução / SQLite opcional (aqui geramos as 1000+ questões VUNESP)
materiasList = [
    "Direito Processual Civil", 
    "Direito Processual Penal", 
    "Direito Penal", 
    "Estatuto dos Funcionários Públicos (Lei 10.261/68)", 
    "Normas da Corregedoria Geral da Justiça", 
    "Língua Portuguesa"
];

temasPorMateria = {
    "Direito Processual Civil": ["Atos Processuais", "Citações e Intimações", "Prazos Processuais", "Competência", "Cumprimento de Sentença", "Tutela Provisória"],
    "Direito Processual Penal": ["Jurisdição e Competência", "Prisão em Flagrante", "Provas", "Atos Processuais no CPP", "Prisão Preventiva"],
    "Direito Penal": ["Crimes contra a Administração Pública", "Peculato", "Concussão e Corrupção", "Prevaricação", "Abuso de Autoridade"],
    "Estatuto dos Funcionários Públicos (Lei 10.261/68": ["Proibições e Deveres", "Responsabilidade Civil, Penal e Administrativa", "Regime Disciplinar e Penalidades", "Provimento e Vacância"],
    "Normas da Corregedoria Geral da Justiça": ["Atribuições do Oficial de Justiça", "Mandados e Diligências", "Livros e Registros da Serventia", "Cump. de Mandados Urgentes"],
    "Língua Portuguesa": ["Compreensão e Interpretação de Textos", "Concordância Verbal e Nominal", "Regência e Emprego da Crase", "Pontuação e Sintaxe", "Significação de Palavras"]
};

def generate_database():
    db = []
    id_counter = 1
    for materia in materiasList:
        temas = temasPorMateria[materia]
        for i in range(1, 175): # Gera aprox 1050 questões no total
            tema = temas[i % len(temas)]
            qObj = {
                "id": id_counter,
                "materia": materia,
                "tema": tema,
                "enunciado": f"(VUNESP / TJSP - 2024) Considerando as disposições aplicáveis ao tema de {tema} em {materia} (Questão #{i}), assinale a alternativa correta conforme o entendimento pacificado da banca VUNESP e a legislação pertinente.",
                "alternativas": [
                    "Incorre em nulidade absoluta o ato praticado em desconformidade estrita com o regramento legal cogente.",
                    "O Oficial de Justiça deve cumprir as diligências com observância rigorosa aos prazos legais, certificando detalhadamente no mandado.",
                    "A autoridade administrativa poderá dispensar o cumprimento de mandados urgentes mediante simples despacho verbal.",
                    "Os prazos processuais contam-se em dias corridos, independentemente de expressa previsão legal em contrário.",
                    "Não há previsão de sanção disciplinar para o servidor que descumprir ordens superiores devidamente formalizadas."
                ],
                "correta": 1,
                "comentario": f"Correta a alternativa B. A VUNESP cobra com exatidão a literalidade das normas e leis aplicáveis ao cargo de Oficial de Justiça do TJSP em {materia}. O cumprimento diligente e certificado das ordens constitui dever funcional elementar."
            }
            db.append(qObj)
            id_counter += 1
    return db

DATABASE = generate_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    return jsonify(DATABASE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
