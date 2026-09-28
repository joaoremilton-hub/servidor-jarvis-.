from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Obtém a chave de API das variáveis de ambiente
API_KEY = os.environ.get("GEMINI_API_KEY")

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

        if not API_KEY:
            return jsonify({'resposta': 'Erro: GEMINI_API_KEY não configurada no Render.'}), 500

        # Inicializa o cliente com o novo SDK
        client = genai.Client(api_key=API_KEY)
        
        prompt = f"Responda à seguinte pergunta ou comando de forma muito direta e curta (máximo 1 ou 2 frases): {query}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return jsonify({'resposta': response.text.strip()})

    except Exception as e:
        return jsonify({'resposta': f'Erro no processamento: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
