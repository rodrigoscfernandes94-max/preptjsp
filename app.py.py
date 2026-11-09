import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# O SDK oficial utiliza a chave de ambiente configurada na Render
# (Você colocará a sua chave AIzaSy... nas variáveis de ambiente da Render)
client = genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/gerar-questao', methods=['POST'])
def gerar_questao():
    try:
        data = request.get_json()
        materia = data.get('materia', 'Língua Portuguesa')
        
        prompt = f"""Gere uma questão inédita de concurso público no rigoroso padrão da banca VUNESP para o cargo de Oficial de Justiça do TJ-SP sobre a matéria: "{materia}".
        Retorne estritamente em formato JSON puro (sem blocos de código markdown como ```json), contendo as chaves exatas:
        - "enunciado": O texto da questão contextualizado.
        - "opcoes": Um array com 4 strings correspondentes às alternativas A, B, C e D.
        - "correta": A letra correta ("A", "B", "C" ou "D").
        - "comentario": A explicação detalhada do gabarito com base na legislação, jurisprudência ou teoria aplicável."""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        texto_resposta = response.text.strip()
        if texto_resposta.startswith("```json"):
            texto_resposta = texto_resposta.replace(/^```json/, "").replace(/```$/, "").strip()
        elif texto_resposta.startswith("```"):
            texto_resposta = texto_resposta.replace(/^```/, "").replace(/```$/, "").strip()

        return jsonify({"status": "sucesso", "dados": texto_resposta})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_ia():
    try:
        data = request.get_json()
        pergunta = data.get('mensagem', '')
        
        prompt = f"""Você é um tutor especialista supremo no concurso de Oficial de Justiça do TJ-SP (banca VUNESP). 
        Responda com rigor técnico absoluto, didática, profundidade e objetividade à seguinte dúvida do aluno (2º Sgt Rodrigo Sá): "{pergunta}"."""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return jsonify({"status": "sucesso", "resposta": response.text})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)