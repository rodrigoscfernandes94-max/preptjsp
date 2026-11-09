import os
import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Banco matriz de estruturação de questões por tópicos do edital VUNESP (TJ-SP)
BANCO_MATRIZ = [
    {
        "materia": "Direito Processual Civil",
        "enunciado": "Nos termos do Código de Processo Civil, a respeito dos atos do Oficial de Justiça e das regras de comunicação processual, assinale a alternativa correta:",
        "alternativas": [
            "O cumprimento de mandados urgentes exige autorização prévia e expressa do Presidente do Tribunal de Justiça.",
            "A citação e a intimação poderão ser realizadas em domingos e feriados, ou fora do horário regulamentar, independentemente de autorização judicial, observada a inviolabilidade domiciliar.",
            "O oficial de justiça poderá arrombar portas e janelas de domicílio residencial por conta própria caso haja fundada suspeita de ocultação.",
            "O mandado judicial de citação perde sua validade em exatos 15 dias corridos caso não seja cumprido.",
            "A certidão lavrada pelo oficial de justiça possui presunção absoluta de veracidade, não admitindo qualquer prova em contrário."
        ],
        "correta": "B",
        "comentario": "Art. 212, § 2º, do CPC: Atos urgentes e diligências fora do horário ou em feriados dispensam autorização judicial, respeitando-se o art. 5º, XI, da CF."
    },
    {
        "materia": "Normas da Corregedoria (TJSP)",
        "enunciado": "Conforme as Normas da Corregedoria Geral da Justiça do Estado de São Paulo (NSCGJ), a respeito da devolução de mandados pelos Oficiais de Justiça, é correto afirmar que:",
        "alternativas": [
            "O prazo geral padrão para o cumprimento e devolução do mandado ao cartório é de 20 dias, ressalvadas as urgências.",
            "O oficial pode reter os mandados em seu poder pelo tempo que julgar necessário para otimizar seu roteiro.",
            "A carga de mandados em caráter de urgência dispensa registro no sistema informatizado oficial.",
            "Em caso de afastamento por férias, o oficial pode repassar seus mandados diretamente para outro colega sem devolvê-los ao cartório.",
            "A certidão negativa por não localização do citando dispensa o detalhamento das diligências realizadas."
        ],
        "correta": "A",
        "comentario": "Conforme as NSCGJ, o prazo regulamentar geral para cumprimento e devolução dos mandados é de 20 dias, ressalvados os prazos menores fixados por lei ou pelo juiz."
    },
    {
        "materia": "Direito Penal",
        "enunciado": "Determinado funcionário público, valendo-se da facilidade que o cargo lhe proporciona, exige de um particular vantagem indevida antes de praticar um ato de ofício. Nos termos do Código Penal, o delito configurado é:",
        "alternativas": [
            "Corrupção passiva.",
            "Peculato-furto.",
            "Concussão.",
            "Prevaricação.",
            "Excesso de exação."
        ],
        "correta": "C",
        "comentario": "O verbo 'exigir' caracteriza o crime de Concussão (art. 316 do CP). A corrupção passiva (art. 317) consuma-se mediante solicitação ou recebimento, sem exigência imperativa."
    },
    {
        "materia": "Direito Processual Penal",
        "enunciado": "De acordo com o Código de Processo Penal, a busca domiciliar sem o consentimento do morador, executada por força de mandado judicial, deve observar a seguinte regra:",
        "alternativas": [
            "Será executada obrigatoriamente durante o período noturno para garantir o elemento surpresa.",
            "Os executores mostrarão e lerão o mandado ao morador antes de penetrar na casa, intimando-o em seguida a abrir a porta.",
            "Pode ser realizada por qualquer cidadão credenciado pela autoridade policial.",
            "Dispensa a presença de testemunhas instrumentárias em qualquer circunstância.",
            "O oficial de justiça possui competência exclusiva e privativa para presidir buscas criminais sem ordem."
        ],
        "correta": "B",
        "comentario": "Art. 245 do CPP: As buscas domiciliares de dia exigem a exibição e leitura prévia do mandado ao morador antes de os executores penetrarem na residência."
    },
    {
        "materia": "Direito Constitucional",
        "enunciado": "Conforme a Constituição Federal de 1988, no tocante aos direitos e garantias fundamentais e à Administração Pública, assinale a alternativa correta:",
        "alternativas": [
            "A casa é asilo inviolável, não podendo nela penetrar sem consentimento do morador, salvo em flagrante delito, desastre, para prestar socorro ou, durante o dia, por determinação judicial.",
            "O cargo de Oficial de Justiça do Tribunal de Justiça é privativo de brasileiro nato.",
            "A criação de associações depende de autorização prévia e expressa do Estado para o seu funcionamento regular.",
            "A prisão civil por dívida é permitida em qualquer hipótese de inadimplência contratual.",
            "A investidura em cargo público dispensa concurso se houver notório saber jurídico."
        ],
        "correta": "A",
        "comentario": "Art. 5º, XI, da CF/88: Traz a regra clássica e exata da inviolabilidade domiciliar e suas exceções constitucionais."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    # Retorna o banco embaralhado para simular um simulado dinâmico
    questoes_embaralhadas = random.sample(BANCO_MATRIZ, len(BANCO_MATRIZ))
    return jsonify(questoes_embaralhadas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
