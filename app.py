import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

QUESTOES = [
    {
        "id": 1,
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
        "comentario": "A alternativa C está correta porque o verbo obedecer é transitivo indireto (exige a preposição 'a': obedecer ao despacho judicial)."
    },
    {
        "id": 2,
        "materia": "Língua Portuguesa",
        "enunciado": "Visando ___ celeridade processual, o juiz determinou ___ expedição de novos mandados, compelindo ___ partes a cumprirem os prazos.",
        "alternativas": [
            "à / à / as",
            "a / à / às",
            "à / a / as",
            "a / a / às",
            "à / à / às"
        ],
        "correta": "A",
        "comentario": "Visar (no sentido de almejar) rege 'a' + artigo 'a' da celeridade = à; Determinar rege preposição + artigo de expedição = à; Compelir é transitivo direto, exigindo apenas o artigo feminino plural = as."
    },
    {
        "id": 3,
        "materia": "Direito Penal",
        "enunciado": "Assinale a alternativa correta acerca dos crimes contra a Administração Pública cometidos por funcionário público:",
        "alternativas": [
            "O crime de peculato-furto ocorre quando o funcionário subtrai ou concorre para que seja subtraído bem público, valendo-se da facilidade que o cargo lhe proporciona, mesmo sem ter a posse direta dele em razão da função.",
            "O crime de concussão exige que o funcionário público receba a vantagem indevida antes de iniciar o ato de ofício.",
            "A corrupção passiva consuma-se unicamente com o efetivo recebimento da vantagem indevida prometida, sendo inadmissível a modalidade tentada.",
            "O peculato culposo exige dolo antecedente à posse do bem público para sua configuração típica.",
            "O funcionário público que concorre para a prática de prevaricação responde pelo mesmo delito, ainda que não possua a qualidade exigida pelo tipo penal."
        ],
        "correta": "E",
        "comentario": "Com base na teoria geral do concurso de pessoas (art. 29 do Código Penal): as circunstâncias e condições de caráter pessoal comunicam-se ao coautor ou partícipe desde que haja ciência."
    },
    {
        "id": 4,
        "materia": "Direito Penal",
        "enunciado": "Determinado indivíduo, com vontade livre e consciente, destrói e inutiliza documentos públicos guardados em repartição policial, os quais faziam prova em inquérito policial em andamento. Nos termos do Código Penal, a conduta praticada configura o crime de:",
        "alternativas": [
            "Supressão de documento.",
            "Dano qualificado contra o patrimônio público.",
            "Favultamento de provas.",
            "Inutilização de edital ou de documento.",
            "Subtração de documento público."
        ],
        "correta": "E",
        "comentario": "Nos termos do artigo 337 do Código Penal, o crime de subtração ou inutilização de livro ou documento consiste em subtrair ou inutilizar documento confiado à custódia de funcionário em razão de ofício."
    },
    {
        "id": 5,
        "materia": "Direito Processual Penal",
        "enunciado": "De acordo com o Código de Processo Penal, a prisão preventiva poderá ser decretada pelo juiz, a requerimento do Ministério Público, do assistente da acusação, ou do querelante, ou por representação da autoridade policial. Sobre os requisitos e fundamentos da prisão preventiva, é correto afirmar que:",
        "alternativas": [
            "A decisão que decretar a prisão preventiva deve ser motivada e fundamentada em receio de perigo abstrato decorrente da gravidade genérica do delito.",
            "A prisão preventiva poderá ser imposta como cumprimento antecipado de pena nos crimes punidos com reclusão em regime fechado.",
            "A existência de indícios suficientes de autoria e a prova da materialidade do delito (fumus commissi delicti) são requisitos essenciais para a decretação da medida.",
            "O juiz poderá decretar a prisão preventiva de ofício durante a fase de investigação policial, independentemente de representação da autoridade policial.",
            "A conversão da prisão em flagrante em preventiva pressupõe obrigatoriamente a realização prévia de audiência de custódia com a presença física obrigatória do promotor de justiça."
        ],
        "correta": "C",
        "comentario": "A alternativa C traz os requisitos indispensáveis (fumus commissi delicti): a prova da materialidade e os indícios suficientes de autoria, previstos no art. 312 do CPP."
    },
    {
        "id": 6,
        "materia": "Direito Processual Civil",
        "enunciado": "Nos termos do Código de Processo Civil, a atuação do oficial de justiça na prática de atos de comunicação e de execução envolve regras específicas de cumprimento de mandados. Assinale a alternativa correta:",
        "alternativas": [
            "O oficial de justiça poderá abater portas e janelas de domicílio residencial, independentemente de autorização judicial, caso haja resistência passiva do executado.",
            "O cumprimento do mandado por oficial de justiça deve ser certificado detalhadamente, descrevendo todas as ocorrências e circunstâncias da diligência, gozando tal certidão de fé pública.",
            "O mandado de citação e intimação perde a validade após o transcurso de 30 dias da sua expedição, caso não seja cumprido.",
            "É facultado ao oficial de justiça recusar o cumprimento de mandado urgente caso este recaia em final de semana.",
            "A citação por oficial de justiça em órgãos públicos federais e estaduais depende de prévia e expressa autorização do chefe da repartição."
        ],
        "correta": "B",
        "comentario": "A certidão lavrada pelo oficial de justiça possui fé pública, gozando de presunção juris tantum (relativa) de veracidade quanto aos fatos por ele testemunhados."
    },
    {
        "id": 7,
        "materia": "Direito Constitucional",
        "enunciado": "Conforme a Constituição Federal de 1988, analise os seguintes institutos e princípios fundamentais: I. O Brasil rege-se nas suas relações internacionais pelos princípios da independência nacional, prevalência dos direitos humanos, autodeterminação dos povos e não-intervenção. II. A soberania, a cidadania, a dignidade da pessoa humana, os valores sociais do trabalho e da livre iniciativa e o pluralismo político constituem os fundamentos da República Federativa do Brasil. III. É assegurado o direito de resposta, proporcional ao agravo, além da indenização por dano material, moral ou à imagem, sendo vedado o anonimato. IV. A criação de associações e, na forma da lei, a de cooperativas dependem de autorização prévia do Estado para o seu funcionamento. Estão corretas apenas as afirmativas:",
        "alternativas": [
            "I, II e III.",
            "I, III e IV.",
            "II, III e IV.",
            "I, II e IV.",
            "I e II apenas."
        ],
        "correta": "A",
        "comentario": "A afirmativa IV está errada porque a criação de associações e cooperativas ocorre independentemente de autorização (art. 5º, XVIII, da CF)."
    },
    {
        "id": 8,
        "materia": "Direito Administrativo",
        "enunciado": "Assinale a alternativa correta a respeito dos poderes administrativos e do uso do poder de polícia:",
        "alternativas": [
            "O poder hierárquico confere à Administração a prerrogativa de aplicar sanções disciplinares a particulares que mantenham contrato administrativo com o órgão público.",
            "O poder disciplinar destina-se a apurar e punir infrações praticadas por servidores públicos ou por pessoas sujeitas à disciplina interna da Administração.",
            "O poder regulamentar é indelegável e pode ser exercido por meio de leis ordinárias aprovadas pelo Poder Executivo.",
            "O poder de polícia consubstancia-se na faculdade de a Administração Pública anular seus próprios atos ilegais, mediante autotutela.",
            "A discricionariedade administrativa afasta por completo a vinculação aos princípios constitucionais da administração pública, como a moralidade e a impessoalidade."
        ],
        "correta": "B",
        "comentario": "O poder disciplinar apura e pune infrações de agentes públicos ou de quem esteja sujeito à disciplina interna da Administração."
    },
    {
        "id": 9,
        "materia": "Direito Civil",
        "enunciado": "Assinale a alternativa correta a respeito da posse e de sua classificação no Código Civil brasileiro:",
        "alternativas": [
            "Considera-se possuidor todo aquele que tem de fato o exercício, pleno ou não, de algum dos poderes inerentes à propriedade.",
            "A posse direta, de quem tem a coisa em seu poder, temporariamente, em virtude de direito pessoal, anula a posse indireta de quem a concedeu.",
            "A posse de boa-fé perde essa característica desde o momento em que haja citação válida em ação possessória, independentemente de o possuidor ter ciência dos vícios do negócio jurídico.",
            "O possuidor turbado, ou esbulhado, não poderá manter-se ou restituir-se por força própria, devendo aguardar ordem judicial prévia.",
            "A posse adquire-se desde o momento em que se manifesta a vontade de possuir, sendo indispensável a apreensão física da coisa."
        ],
        "correta": "A",
        "comentario": "Traz a regra exata do artigo 1.196 do Código Civil sobre a definição de possuidor."
    },
    {
        "id": 10,
        "materia": "Informática",
        "enunciado": "No sistema operacional Microsoft Windows 10/11, o atalho de teclado utilizado para alternar rapidamente entre as janelas de aplicativos abertos é:",
        "alternativas": [
            "Ctrl + C",
            "Alt + Tab",
            "Windows + L",
            "Ctrl + Shift + Esc",
            "Alt + F4"
        ],
        "correta": "B",
        "comentario": "Alt + Tab alterna entre as janelas/aplicativos abertos. Windows+L bloqueia a tela; Alt+F4 fecha o aplicativo."
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
