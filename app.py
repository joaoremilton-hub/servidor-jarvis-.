import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Configura o cliente da SDK oficial do Google
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis IA rodando!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        prompt = data.get('prompt', 'Ola')

        # 1. Tenta explicitamente os modelos recomendados da geração atual
        modelos_prioritarios = [
            'gemini-3.6-flash',
            'gemini-3.5-flash',
            'gemini-2.5-flash'
        ]

        for model_name in modelos_prioritarios:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return jsonify({'response': response.text})
            except Exception:
                continue

        # 2. Se nenhum da lista responder, consulta dinamicamente o primeiro ativo da sua chave
        available_models = [m.name for m in client.models.list()]
        if available_models:
            target_model = available_models[0]
            response = client.models.generate_content(
                model=target_model,
                contents=prompt
            )
            return jsonify({'response': response.text})

        return jsonify({'error': 'Nenhum modelo ativo encontrado na sua API Key'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
