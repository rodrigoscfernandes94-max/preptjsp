import os
from flask import Flask, jsonify, render_template
import google.generativeai as genai
import json

app = Flask(__name__)

# Configuração da chave de API
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

QUESTOES_INICIAIS = [
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
        "comentario": "Art. 212, § 2º, do CPC: A citação e a intimação poderão ser realizadas em domingos e feriados, ou fora do horário estabelecido no caput, independentemente de autorização judicial."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questoes', methods=['GET'])
def get_questoes():
    return jsonify(QUESTOES_INICIAIS)

@app.route('/api/gerar-questao-ia', methods=['GET'])
def gerar_questao_ia():
    if not API_KEY:
        return jsonify({
            "erro": "Chave GEMINI_API_KEY não configurada no Render. Adicione-a na aba Environment do seu Web Service."
        }), 400
    
    try:
        # Chamada direta ao modelo para gerar a questão nível VUNESP
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = """
        Atue como uma banca examinadora de alta exigência (padrão VUNESP) para o concurso de Oficial de Justiça do TJ-SP.
        Gere uma questão inédita e de nível técnico avançado sobre Direito Processual Civil, Normas da Corregedoria do TJSP, Direito Penal ou Direito Constitucional.
        
        Retorne APENAS um objeto JSON puro, sem blocos de código markdown, exatamente com esta estrutura:
        {
          "materia": "Nome da Matéria",
          "enunciado": "Texto completo da questão complexa estilo VUNESP",
          "alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D", "Alternativa E"],
          "correta": "Letra maiúscula da resposta (A, B, C, D ou E)",
          "comentario": "Fundamentação legal detalhada explicando o gabarito e o erro das demais."
        }
        """
        
        response = model.generate_content(prompt)
        texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
        questao_json = json.loads(texto_limpo)
        
        return jsonify(questao_json)
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar com IA: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
