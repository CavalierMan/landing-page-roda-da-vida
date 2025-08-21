from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Inicializa o aplicativo Flask
app = Flask(__name__)
# Habilita o CORS para permitir que nosso frontend (em outro endereço) se comunique com o backend
CORS(app)

# Função para se conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Define a rota/endpoint para receber os e-mails
# methods=['POST'] significa que esta rota só aceita requisições do tipo POST
@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Pega o e-mail do corpo da requisição JSON enviada pelo frontend
    email = request.json.get('email', None)

    # Validação simples para ver se o e-mail foi enviado
    if not email:
        return jsonify({'status': 'error', 'message': 'E-mail não fornecido.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Tenta inserir o novo e-mail na tabela
        cursor.execute('INSERT INTO emails (email_address) VALUES (?)', (email,))
        conn.commit()
        status_message = {'status': 'success', 'message': 'E-mail cadastrado com sucesso!'}
        status_code = 201
    except sqlite3.IntegrityError:
        # sqlite3.IntegrityError ocorre quando uma regra é violada, como a de e-mail ÚNICO (UNIQUE)
        status_message = {'status': 'error', 'message': 'Este e-mail já está cadastrado.'}
        status_code = 409
    except Exception as e:
        # Captura qualquer outro erro que possa acontecer
        status_message = {'status': 'error', 'message': f'Ocorreu um erro no servidor: {e}'}
        status_code = 500
    finally:
        # Garante que a conexão com o banco de dados seja sempre fechada
        conn.close()

    # Retorna uma resposta em formato JSON para o frontend
    return jsonify(status_message), status_code

# Linha padrão para rodar o servidor quando executamos o script diretamente
if __name__ == '__main__':
    app.run(debug=True)