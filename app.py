import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Inicializa o cliente oficial da biblioteca google-genai
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis IA rodando!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'response': 'Prompt vazio'}), 400

        # Seleciona dinamicamente o modelo ativo disponivel na conta
        available_models = [m.name for m in client.models.list()]
        target_model = available_models[0] if available_models else 'gemini-2.5-flash'

        response = client.models.generate_content(
            model=target_model,
            contents=prompt
        )

        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error_detalhado': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
