import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configura a chave da API do Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_active_model():
    try:
        # Busca dinamicamente um modelo disponivel que suporte generateContent
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name:
                    return genai.GenerativeModel(m.name)
        # Fallback para o modelo padrao caso nao liste
        return genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        print(f"Erro ao buscar modelo: {e}")
        return genai.GenerativeModel('gemini-2.5-flash')

model = get_active_model()

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis IA rodando perfeitamente!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'response': 'Prompt vazio'}), 400
        
        # Gera a resposta utilizando o modelo ativo selecionado
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
