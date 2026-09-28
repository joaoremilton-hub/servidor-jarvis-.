from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configura a chave de API do Gemini (Coloque sua chave nas variáveis de ambiente do Render)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis com IA Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo enviado.'}), 400

        # Usa o modelo mais rápido e leve do Google Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"Responda a seguinte pergunta de forma muito direta, resumida e precisa em 1 ou 2 frases: {query}"
        
        response = model.generate_content(prompt)
        resposta_texto = response.text.strip()
        
        return jsonify({'resposta': resposta_texto})

    except Exception as e:
        return jsonify({'resposta': f'Erro ao processar IA: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
