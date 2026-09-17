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
        prompt = data.get('prompt', 'Ola')
        if not prompt:
            return jsonify({'response': 'Prompt vazio'}), 400

        # Busca a lista de modelos disponiveis diretamente na conta do Google
        models_list = list(client.models.list())
        
        # Filtra apenas modelos que suportam geração de texto
        valid_models = [
            m.name for m in models_list 
            if 'generateContent' in getattr(m, 'supported_generation_methods', [])
        ]

        if not valid_models:
            return jsonify({'error': 'Nenhum modelo disponivel para esta chave de API.'}), 500

        # Pega o primeiro modelo valido retornado pela API da sua conta
        selected_model = valid_models[0]

        # Envia o prompt para o modelo identificado
        response = client.models.generate_content(
            model=selected_model,
            contents=prompt
        )

        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error_detalhado': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
