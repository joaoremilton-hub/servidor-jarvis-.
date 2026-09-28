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

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        # 1. Tenta primeira busca na Wikipedia pelo termo exato
        search_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
        search_res = requests.get(search_url, headers=headers, timeout=5).json()
        search_results = search_res.get('query', {}).get('search', [])

        if search_results:
            exact_title = search_results[0]['title']
            summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(exact_title)}"
            summary_res = requests.get(summary_url, headers=headers, timeout=5)
            if summary_res.status_code == 200:
                resumo = summary_res.json().get('extract', '')
                if resumo:
                    return jsonify({'resposta': resumo})

        # 2. Se nao achar na Wikipedia, usa a API DuckDuckGo Instant Answer (API Oficial sem bloqueio)
        api_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1&skip_disambig=1"
        res_ddg = requests.get(api_url, headers=headers, timeout=5).json()
        
        abstract = res_ddg.get('AbstractText', '')
        if abstract:
            return jsonify({'resposta': abstract})
            
        heading = res_ddg.get('Heading', '')
        related = res_ddg.get('RelatedTopics', [])
        if related and 'Text' in related[0]:
            return jsonify({'resposta': related[0]['Text']})

        return jsonify({'resposta': f'Não encontrei resumo direto para "{query}". Tente especificar melhor.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
