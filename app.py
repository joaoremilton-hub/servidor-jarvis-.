import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Inicializa o cliente oficial da biblioteca google-genai
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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

        # Lista os modelos ativos disponiveis para a sua chave e seleciona o primeiro compativel
        available_models = [
            m.name for m in client.models.list() 
            if 'generateContent' in getattr(m, 'supported_generation_methods', [])
        ]
        
        # Prefere modelos flash ativos, senao usa o primeiro disponivel
        target_model = next((m for m in available_models if 'flash' in m), available_models[0] if available_models else 'gemini-2.5-flash')

        response = client.models.generate_content(
            model=target_model,
            contents=prompt
        )

        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
