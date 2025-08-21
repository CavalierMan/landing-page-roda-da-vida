import sqlite3

# Conecta ao banco de dados (se não existir, ele será criado)
connection = sqlite3.connect('database.db')

# Cria um "cursor", que é o objeto que executa os comandos
cursor = connection.cursor()

# Executa o comando SQL para criar nossa tabela de e-mails
# IF NOT EXISTS garante que não tentaremos criar a tabela se ela já existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_address TEXT NOT NULL UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Salva (commita) as mudanças
connection.commit()

# Fecha a conexão
connection.close()

print("Banco de dados 'database.db' e tabela 'emails' criados com sucesso!")