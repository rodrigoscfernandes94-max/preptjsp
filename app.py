import os
import json
from flask import Flask, render_template, request, jsonify
from google import genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)

# Escopos necessários para acessar os modelos de IA com sua conta Google
SCOPES = ['https://www.googleapis.com/auth/generative-ai']

def obter_cliente_ia():
    """Autentica dinamicamente usando a sua conta Google pessoal"""
    creds = None
    token_path = 'token.json'
    
    # Verifica se já temos um token salvo localmente
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # Se não houver credenciais válidas, tentamos via variável de ambiente ou fluxo local
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
                
        if not creds:
            # Caso esteja rodando na nuvem (Render), usamos a autenticação padrão do ambiente
            if os.environ.get('RENDER'):
                # Na Render, utilizamos a credencial padrão configurada por login de serviço ou variável
                return genai.Client()
            
            # Se estiver rodando localmente para teste, você pode usar um client_secret.json da sua conta
            if os.path.exists('client_secret.json'):
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

    if creds:
        return genai.Client(credentials=creds)
    else:
        # Fallback seguro para o cliente padrão do SDK
        return genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/gerar-questao', methods=['POST'])
def gerar_questao():
    try:
        data = request.get_json()
        materia = data.get('materia', 'Língua Portuguesa')
        
        client = obter_cliente_ia()
        
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
            texto_resposta = texto_resposta.replace("```json", "").replace("```", "").strip()
        elif texto_resposta.startswith("```"):
            texto_resposta = texto_resposta.replace("```", "").strip()

        return jsonify({"status": "sucesso", "dados": texto_resposta})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_ia():
    try:
        data = request.get_json()
        pergunta = data.get('mensagem', '')
        
        client = obter_cliente_ia()
        
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
    port = int(os.environ.get('PORT', 10000))
    app.app.run(host='0.0.0.0', port=port)
