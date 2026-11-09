import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Base de questões blindada em memória (sem dependência de arquivos externos ou banco de dados físico)
QUESTOES_MEMORIA = [
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
    },
    {
        "id": 3,
        "materia": "Direito Constitucional",
        "enunciado": "São princípios expressamente relacionados à Administração Pública no art. 37 da Constituição Federal:",
        "alternativas": [
            "legalidade, pessoalidade, sigilo, eficiência e supremacia.",
            "legalidade, impessoalidade, moralidade, publicidade e eficiência.",
            "moralidade, segredo, hierarquia, publicidade e eficiência.",
            "legalidade, informalidade, publicidade, pessoalidade e eficiência.",
            "apenas legalidade e eficiência."
        ],
        "correta": "B",
        "comentario": "Mnemônico LIMPE: Legalidade, Impessoalidade, Moralidade, Publicidade e Eficiência."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    try:
        return jsonify(QUESTOES_MEMORIA)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
