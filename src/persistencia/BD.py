import sqlite3 #Importa a biblioteca do Python que permite trabalhar com bancos SQLite.
from pathlib import Path

# Localiza a pasta principal do projeto.
PASTA_PROJETO = Path(__file__).resolve().parents[2]

# Define onde o arquivo do banco de dados será armazenado.
CAMINHO_BANCO = PASTA_PROJETO / "financas.db" 

def conectar_banco():
    # Abre uma conexão com o SQLite.
    # Se o arquivo ainda não existir, o SQLite poderá criá-lo.
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Ativa a verificação das relações entre tabelas.
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    try:
        # Cria a tabela de cartões, caso ela ainda não exista, com 4 colunas
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS cartoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dia_fechamento INTEGER NOT NULL,
                dia_vencimento INTEGER NOT NULL
            )
        """)

        # TABELA 2: COMPRAS
        # Guarda as informações gerais das compras. Cada compra pertence a um cartão cadastrado.
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cartao_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                identificacao_fatura TEXT NOT NULL DEFAULT '',
                valor_total_centavos INTEGER NOT NULL,
                data_compra TEXT NOT NULL,
                quantidade_parcelas INTEGER NOT NULL,

                FOREIGN KEY (cartao_id)
                    REFERENCES cartoes(id)
            )
        """)

        # TABELA 3: PARCELAS
        # Guarda cada parcela gerada para uma compra. Os valores são armazenados em centavos.
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS parcelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                numero INTEGER NOT NULL,
                valor_centavos INTEGER NOT NULL,
                vencimento TEXT NOT NULL,

                FOREIGN KEY (compra_id)
                    REFERENCES compras(id),

                UNIQUE (compra_id, numero)
            )
        """)

        # Impede cartões com nomes duplicados.
        # LOWER ignora diferenças entre letras maiúsculas e minúsculas.
        # TRIM remove espaços no início e no final.
        # UNIQUE impede a repetição do nome normalizado.
        conexao.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_cartoes_nome_unico
            ON cartoes (LOWER(TRIM(nome)))
        """)

        # Confirma as alterações realizadas no banco.
        conexao.commit()
    finally:
        # Fecha a conexão mesmo se ocorrer algum erro.
        conexao.close()