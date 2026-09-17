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

        # Lista de modelos suportados para tentar na ordem de preferencia
        models_to_try = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-001',
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest'
        ]

        last_error = None
        # Tenta cada modelo ate encontrar um disponivel para a sua chave
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return jsonify({'response': response.text})
            except Exception as err:
                last_error = err
                continue

        # Se nenhum da lista funcionar, lanca o ultimo erro
        raise last_error

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
