from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def resolver_matematica(expressao):
    # Permite apenas numeros e operadores matematicos simples por seguranca
    expressao_limpa = re.sub(r'[^0-9\+\-\*\/\.\(\)\s]', '', expressao)
    if expressao_limpa and any(c in expressao_limpa for c in '+-*/'):
        try:
            # Avalia a conta matematica
            resultado = eval(expressao_limpa, {"__builtins__": None}, {})
            return f"Resultado: {resultado}"
        except:
            return None
    return None

@app.route('/', methods=['GET'])
def home():
    return "Servidor Jarvis de Buscas e Calculo Ativo!"

@app.route('/busca', methods=['POST'])
def busca():
    try:
        data = request.get_json(force=True)
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'resposta': 'Nenhum termo enviado.'}), 400

        # 1. TENTA RESOLVER COMO MATEMÁTICA
        resultado_math = resolver_matematica(query)
        if resultado_math:
            return jsonify({'resposta': resultado_math})

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # 2. TENTA API INSTANTÂNEA DO DUCKDUCKGO
        ddg_api = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1&skip_disambig=1"
        try:
            res_ddg = requests.get(ddg_api, headers=headers, timeout=5).json()
            abstract = res_ddg.get('AbstractText', '')
            if abstract:
                return jsonify({'resposta': abstract})
        except:
            pass

        # 3. TENTA BUSCA HTML DE RESULTADOS NA WEB
        url = "https://lite.duckduckgo.com/lite/"
        payload = {'q': query}
        res = requests.post(url, data=payload, headers=headers, timeout=8)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            snippets = soup.find_all('td', class_='result-snippet')
            
            if snippets:
                texto = snippets[0].get_text(strip=True)
                texto = re.sub(r'\s+', ' ', texto)
                return jsonify({'resposta': texto})

        # 4. FALLBACK WIKIPEDIA
        wiki_url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
        wiki_res = requests.get(wiki_url, headers=headers, timeout=5).json()
        results = wiki_res.get('query', {}).get('search', [])

        if results:
            title = results[0]['title']
            summary_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title)}"
            summary_res = requests.get(summary_url, headers=headers, timeout=5)
            if summary_res.status_code == 200:
                resumo = summary_res.json().get('extract', '')
                if resumo:
                    return jsonify({'resposta': resumo})

        return jsonify({'resposta': f'Não encontrei informações sobre "{query}".'})

    except Exception as e:
        return jsonify({'resposta': f'Erro no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
