import os
import tempfile
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configura a chave da API do Gemini vinda do ambiente na nuvem
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Usamos o modelo rápido e gratuito
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis IA rodando perfeitamente!", 200

# Rota para receber PERGUNTAS EM TEXTO (para testes)
@app.route('/ask-text', methods=['POST'])
def ask_text():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'Texto vazio'}), 400

        response = model.generate_content(f"Responda de forma direta e curta em português: {prompt}")
        return jsonify({'status': 'sucesso', 'resposta': response.text}), 200
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

# Rota principal para receber ÁUDIO RAW/WAV vindo do ESP32
@app.route('/ask-audio', methods=['POST'])
def ask_audio():
    try:
        # Pega os bytes brutos do áudio enviados pelo ESP32
        audio_data = request.data
        if not audio_data:
            return jsonify({'error': 'Nenhum dado de áudio recebido'}), 400

        # Salva o arquivo temporário de áudio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        # Envia o áudio diretamente para a API do Gemini processar
        audio_file = genai.upload_file(path=temp_audio_path)
        response = model.generate_content([
            "Ouça este áudio do usuário e responda de forma muito curta, direta e em português:", 
            audio_file
        ])

        # Deleta o arquivo temporário
        os.remove(temp_audio_path)

        return jsonify({
            'status': 'sucesso',
            'resposta': response.text
        }), 200

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)