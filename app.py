from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Servidor de Buscas Web Jarvis Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo enviado.'}), 400

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # 1. TENTA BUSCA GERAL NA WEB (DuckDuckGo Lite)
        url = "https://lite.duckduckgo.com/lite/"
        payload = {'q': query}
        
        res = requests.post(url, data=payload, headers=headers, timeout=8)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Extrai os snippets de texto dos resultados da pesquisa web
            snippets = soup.find_all('td', class_='result-snippet')
            
            if snippets:
                # Pega o primeiro resultado da web e limpa espaços extras
                texto_resultado = snippets[0].get_text(strip=True)
                texto_resultado = re.sub(r'\s+', ' ', texto_resultado)
                return jsonify({'resposta': texto_resultado})

        # 2. SE NÃO ACHAR NA WEB, BUSCA RESUMO NA WIKIPEDIA COMO FALLBACK
        wiki_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
        wiki_res = requests.get(wiki_url, headers=headers, timeout=5).json()
        search_results = wiki_res.get('query', {}).get('search', [])

        if search_results:
            exact_title = search_results[0]['title']
            summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(exact_title)}"
            summary_res = requests.get(summary_url, headers=headers, timeout=5)
            if summary_res.status_code == 200:
                resumo = summary_res.json().get('extract', '')
                if resumo:
                    return jsonify({'resposta': resumo})

        return jsonify({'resposta': f'Não encontrei resultados para "{query}" na web.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro na busca web: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
