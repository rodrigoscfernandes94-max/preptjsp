import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

QUESTOES = [
    {
        "id": 1,
        "materia": "Língua Portuguesa",
        "enunciado": "Embora o oficial tivesse recebido a ordem com antecedência, somente a cumpriu após nova determinação. A palavra “Embora” estabelece relação de:",
        "alternativas": [
            "causa.",
            "conclusão.",
            "concessão.",
            "condição.",
            "finalidade."
        ],
        "correta": "C",
        "comentario": "A conjunção 'embora' introduz oração subordinada adverbial concessiva."
    },
    {
        "id": 2,
        "materia": "Direito Processual Civil",
        "enunciado": "A citação válida, no processo civil:",
        "alternativas": [
            "não produz qualquer efeito processual.",
            "induz litispendência, torna litigiosa a coisa e constitui em mora o devedor, ressalvadas as hipóteses legais.",
            "encerra automaticamente o processo.",
            "impede qualquer acordo.",
            "substitui a sentença."
        ],
        "correta": "B",
        "comentario": "Conforme o art. 240 do CPC, a citação válida induz litispendência e constitui em mora o devedor."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    return jsonify(QUESTOES)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
