import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Banco robusto de questões de nível exato VUNESP para Oficial de Justiça TJSP
QUESTOES_TJSP = [
    {
        "id": 1,
        "materia": "Direito Processual Civil",
        "enunciado": "Nos termos do Código de Processo Civil, as citações e intimações poderão ser realizadas em domingos e feriados, ou fora do horário regulamentar (entre 6 e 20 horas):",
        "alternativas": [
            "Apenas se houver autorização prévia expressa do Corregedor Geral de Justiça.",
            "Independentemente de autorização judicial, observado o disposto no art. 5º, XI, da Constituição Federal.",
            "Sendo vedada qualquer diligência nesses períodos sob pena de nulidade absoluta do ato.",
            "Desde que haja pagamento antecipado de taxa de urgência em dobro pela parte autora.",
            "Somente se o citando concordar expressamente por escrito com a diligência."
        ],
        "correta": "B",
        "comentario": "Art. 212, § 2º, do CPC: A citação e a intimação poderão ser realizadas em domingos e feriados, ou fora do horário estabelecido no caput, independentemente de autorização judicial, observada a inviolabilidade do domicílio."
    },
    {
        "id": 2,
        "materia": "Normas da Corregedoria (TJSP)",
        "enunciado": "Conforme o Tomo I das Normas Judiciais da Corregedoria Geral da Justiça de SP, os mandados distribuídos aos Oficiais de Justiça devem ser cumpridos e devolvidos ao cartório no prazo de:",
        "alternativas": [
            "24 horas em qualquer situação de urgência.",
            "10 dias corridos a contar da carga.",
            "20 (vinte) dias, ressalvadas as urgências e prazos menores fixados pelo juiz ou por lei.",
            "30 dias improrrogáveis para todas as comarcas do Estado.",
            "60 dias."
        ],
        "correta": "C",
        "comentario": "Conforme as NSCGJ, o prazo geral padrão para cumprimento e devolução do mandado pelo Oficial de Justiça é de 20 dias, ressalvadas as urgências e determinações judiciais específicas."
    },
    {
        "id": 3,
        "materia": "Língua Portuguesa",
        "enunciado": "Assinale a alternativa em que a regência do verbo obedecer está empregada em estrita conformidade com a norma-padrão da língua portuguesa:",
        "alternativas": [
            "O oficial de justiça precavido obedeceu rigorosamente os prazos processuais estabelecidos no mandado.",
            "O servidor público deve obediência às normas estatutárias, obedecendo-as com rigor no cotidiano da vara.",
            "A diligência urgente exigia que o oficial obedecesse ao despacho judicial sem questionamentos.",
            "O réu devidamente citado obedeceu a ordem de comparecimento expedida pelo juiz titular.",
            "Quem desrespeitar ou não obedecer o mandado de prisão incorrerá em crime de desobediência."
        ],
        "correta": "C",
        "comentario": "O verbo obedecer é transitivo indireto (exige a preposição 'a': obedecer ao despacho judicial). As demais erraram por usá-lo como transitivo direto ou omitir a preposição."
    },
    {
        "id": 4,
        "materia": "Direito Penal",
        "enunciado": "O funcionário público que exige, para si ou para outrem, direta ou indiretamente, ainda que fora da função ou antes de assumi-la, mas em razão dela, vantagem indevida, comete o crime de:",
        "alternativas": [
            "Corrupção passiva.",
            "Peculato-desvio.",
            "Concussão.",
            "Prevaricação.",
            "Condescendência criminosa."
        ],
        "correta": "C",
        "comentario": "O verbo 'EXIGIR' caracteriza o crime de Concussão (art. 316 do Código Penal). Se o verbo fosse 'solicitar ou receber', caracterizaria Corrupção Passiva (art. 317)."
    },
    {
        "id": 5,
        "materia": "Direito Processual Penal",
        "enunciado": "De acordo com o Código de Processo Penal, a busca domiciliar sem consentimento do morador será realizada durante o dia e exigirá que os executores:",
        "alternativas": [
            "Arrombem imediatamente o imóvel para garantir o elemento surpresa.",
            "Mostrem e leiam o mandado ao morador antes de penetrar na casa, intimando-o a abrir a porta.",
            "Aguardem a presença obrigatória do promotor de justiça no local.",
            "Dispensam qualquer formalidade caso o portão esteja destrancado.",
            "Realizem a diligência exclusivamente entre 00h e 06h."
        ],
        "correta": "B",
        "comentario": "Art. 245 do CPP: Antes de penetrarem na casa, os executores mostrarão e lerão o mandado ao morador, intimando-o em seguida a abrir a porta."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    return jsonify(QUESTOES_TJSP)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
