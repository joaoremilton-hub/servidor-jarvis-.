from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis com IA Direta Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo enviado.'}), 400

        if not API_KEY:
            return jsonify({'resposta': 'Erro: GEMINI_API_KEY não configurada no Render.'}), 500

        # Chamada REST direta à API do Gemini (sem bibliotecas pesadas)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        prompt_text = f"Responda à seguinte pergunta de forma muito direta e curta em 1 ou 2 frases: {query}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            res_json = response.json()
            try:
                text_response = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
                return jsonify({'resposta': text_response})
            except (KeyError, IndexError):
                return jsonify({'resposta': 'Não consegui processar a resposta da IA.'})
        else:
            return jsonify({'resposta': f'Erro na API Gemini (Código {response.status_code}). Verificar chave.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
