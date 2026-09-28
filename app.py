from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Servidor de Buscas Jarvis Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo para buscar.'}), 400

        # Faz a chamada direta a API REST oficial da Wikipedia em Portugues
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        headers = {'User-Agent': 'ESP32JarvisBot/1.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            wiki_data = response.json()
            # Pega o resumo da pagina
            resumo = wiki_data.get('extract', 'Sem resumo disponível.')
            return jsonify({'resposta': resumo})
        elif response.status_code == 404:
            return jsonify({'resposta': f'Não encontrei resultados para "{query}" na Wikipedia.'})
        else:
            return jsonify({'resposta': 'Erro ao consultar a base de dados da Wikipedia.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
