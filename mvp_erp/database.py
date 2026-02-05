"""
Módulo de conexão e configuração do banco de dados SQLite.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'mvp.db')


def get_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de empresas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            cnpj TEXT,
            ativo INTEGER DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de operações (compra/venda)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('COMPRA', 'VENDA')),
            empresa_id INTEGER NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            prazo_dias INTEGER DEFAULT 7,
            data_operacao DATE NOT NULL,
            data_vencimento DATE NOT NULL,
            data_liquidacao DATE,
            status TEXT DEFAULT 'ABERTO' CHECK(status IN ('ABERTO', 'LIQUIDADO', 'CANCELADO')),
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")
