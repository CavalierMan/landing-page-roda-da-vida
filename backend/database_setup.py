import sqlite3

# Conecta ao banco de dados
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# --- Tabela de E-mails (da Landing Page) ---
# Apenas garantindo que ela ainda exista, não vai criar de novo.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_address TEXT NOT NULL UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# --- NOVA TABELA: Usuários do App ---
# Irá guardar as informações de login.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# --- NOVA TABELA: Pontuações da Roda da Vida ---
# Irá guardar as notas de cada pilar para cada usuário.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wheel_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        carreira INTEGER DEFAULT 0,
        financas INTEGER DEFAULT 0,
        saude INTEGER DEFAULT 0,
        familia INTEGER DEFAULT 0,
        amor INTEGER DEFAULT 0,
        lazer INTEGER DEFAULT 0,
        espiritual INTEGER DEFAULT 0,
        amigos INTEGER DEFAULT 0,
        intelectual INTEGER DEFAULT 0,
        emocional INTEGER DEFAULT 0,
        profissional INTEGER DEFAULT 0,
        proposito INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')


# Salva (commita) as mudanças
connection.commit()

# Fecha a conexão
connection.close()

print("Banco de dados verificado e atualizado com as tabelas 'users' e 'wheel_scores'!")