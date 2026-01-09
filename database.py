import sqlite3

def init_db():
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()
    # Cria a tabela de autorizados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autorizados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            nome_morador TEXT NOT NULL,
            tipo TEXT NOT NULL -- 'MORADOR' ou 'VISITANTE'
        )
    ''')
    # Insere alguns dados de teste (opcional)
    try:
        cursor.execute("INSERT INTO autorizados (placa, nome_morador, tipo) VALUES ('OTM2X22', 'Carlos Silva', 'MORADOR')")
        cursor.execute("INSERT INTO autorizados (placa, nome_morador, tipo) VALUES ('RIO2A18', 'Ana Souza', 'VISITANTE')")
        cursor.execute("INSERT INTO autorizados (placa, nome_morador, tipo) VALUES ('BRA0S17', 'Jose Silva', 'VISITANTE')")
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Placa já cadastrada
    conn.close()

def verificar_placa(placa):
    """Retorna o nome do morador se autorizado, senão None"""
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()
    # Limpa espaços e deixa em maiúsculo para evitar erros
    placa_limpa = placa.strip().upper()
    cursor.execute("SELECT nome_morador FROM autorizados WHERE placa = ?", (placa_limpa,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado com sucesso.")