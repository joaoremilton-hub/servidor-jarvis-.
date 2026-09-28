from flask import Flask, request, jsonify
import wikipedia

# Define o idioma da Wikipedia para português
wikipedia.set_lang("pt")

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

        # Busca um resumo rápido na Wikipedia (limite de 2 frases)
        resumo = wikipedia.summary(query, sentences=2)
        return jsonify({'resposta': resumo})

    except wikipedia.exceptions.DisambiguationError as e:
        # Se houver múltiplos significados, pega o primeiro termo
        try:
            resumo = wikipedia.summary(e.options[0], sentences=2)
            return jsonify({'resposta': resumo})
        except:
            return jsonify({'resposta': f'A busca por "{query}" retornou vários resultados. Seja mais específico.'})
            
    except wikipedia.exceptions.PageError:
        return jsonify({'resposta': f'Não encontrei informações sobre "{query}" na web.'})
        
    except Exception as e:
        return jsonify({'resposta': f'Erro ao realizar busca: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
