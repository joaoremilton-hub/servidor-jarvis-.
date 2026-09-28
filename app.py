from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Servidor de Buscas Geral Jarvis Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo para buscar.'}), 400

        # Faz requisição direta a versão Lite do DuckDuckGo (rápida e leve)
        url = "https://html.duckduckgo.com/html/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        payload = {'q': query}
        
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extrai os trechos (snippets) de texto dos resultados da pesquisa
            snippets = soup.find_all('a', class_='result__snippet')
            
            if snippets:
                # Pega o resumo do primeiro resultado encontrado na Web
                resumo = snippets[0].get_text(strip=True)
                return jsonify({'resposta': resumo})
            else:
                return jsonify({'resposta': f'Não encontrei resultados para "{query}" na web.'})
        else:
            return jsonify({'resposta': 'Erro ao acessar o motor de busca na web.'})

    except Exception as e:
        return jsonify({'resposta': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
