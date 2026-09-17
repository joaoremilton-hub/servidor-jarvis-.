import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configura a chave de API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis IA rodando!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        prompt = data.get('prompt', 'Ola')

        # Tenta a lista de modelos ativos um a um automaticamente
        modelos = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
        
        for m in modelos:
            try:
                model = genai.GenerativeModel(m)
                response = model.generate_content(prompt)
                return jsonify({'response': response.text})
            except Exception:
                continue

        return jsonify({'error': 'Nenhum modelo respondeu'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
