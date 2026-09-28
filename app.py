from flask import Flask, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Servidor de Buscas Jarvis Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '')
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo para buscar.'}), 400

        # Faz a pesquisa rápida na web sem usar IA
        results = list(DDGS().text(query, max_results=1))
        
        if results:
            resumo = results[0]['body']
            return jsonify({'resposta': resumo})
        else:
            return jsonify({'resposta': 'Não encontrei resultados para essa pesquisa na web.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro ao realizar busca: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
