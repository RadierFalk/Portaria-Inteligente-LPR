import sqlite3

def init_db():
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()
    # Criando a tabela com todos os novos campos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moradores (
            placa TEXT PRIMARY KEY,
            nome TEXT,
            telefone TEXT,
            endereco TEXT,
            modelo TEXT,
            marca TEXT
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_usuario(placa, nome, telefone, endereco, modelo, marca):
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO moradores VALUES (?, ?, ?, ?, ?, ?)', 
                       (placa.upper(), nome, telefone, endereco, modelo, marca))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def buscar_dados_completos(placa):
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM moradores WHERE placa = ?', (placa,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado # Retorna a linha inteira ou None