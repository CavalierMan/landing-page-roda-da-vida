from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
# ADICIONE ESTA LINHA AQUI
from werkzeug.security import generate_password_hash, check_password_hash

# O resto do seu código continua abaixo...
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
# --- ROTA PARA REGISTRO DE NOVOS USUÁRIOS DO APP ---
@app.route('/register', methods=['POST'])
def register():
    # Pega o e-mail e a senha da requisição
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validação simples
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'E-mail e senha são obrigatórios.'}), 400

    # Cria um "hash" seguro da senha. NUNCA salvamos senhas em texto puro!
    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Tenta inserir o novo usuário na tabela 'users'
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (?, ?)', (email, password_hash))
        conn.commit()
        status_message = {'status': 'success', 'message': 'Usuário criado com sucesso!'}
        status_code = 201
    except sqlite3.IntegrityError:
        # Este erro acontece se o e-mail (que é UNIQUE) já existir
        status_message = {'status': 'error', 'message': 'Este e-mail já foi cadastrado.'}
        status_code = 409
    except Exception as e:
        status_message = {'status': 'error', 'message': f'Ocorreu um erro no servidor: {e}'}
        status_code = 500
    finally:
        conn.close()
    
    return jsonify(status_message), status_code
# --- ROTA PARA LOGIN DE USUÁRIOS EXISTENTES ---
@app.route('/login', methods=['POST'])
def login():
    # Pega o e-mail e a senha da requisição
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validação simples
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'E-mail e senha são obrigatórios.'}), 400
    
    # Abre a conexão com o banco de dados
    conn = get_db_connection()
    cursor = conn.cursor()

    # Procura por um usuário com o e-mail fornecido
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone() # Pega o primeiro (e único) resultado

    # Fecha a conexão o mais rápido possível
    conn.close()

    # Verifica se o usuário existe E se a senha está correta
    if user and check_password_hash(user['password_hash'], password):
        # Se ambos estiverem corretos, o login é um sucesso
        status_message = {'status': 'success', 'message': 'Login realizado com sucesso!'}
        status_code = 200
    else:
        # Se o usuário não existe ou a senha está errada
        status_message = {'status': 'error', 'message': 'Credenciais inválidas.'}
        status_code = 401

    return jsonify(status_message), status_code
if __name__ == '__main__':
    app.run(debug=True)