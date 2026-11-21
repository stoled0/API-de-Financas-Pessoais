import sqlite3
from src.persistencia.BD import conectar_banco

conexao = conectar_banco()

try:
    # Tenta cadastrar outro Nubank.
    conexao.execute(
        """
        INSERT INTO cartoes (
            nome,
            dia_fechamento,
            dia_vencimento
        )
        VALUES (?, ?, ?)
        """,
        (" NUBANK ", 3, 10)
    )

    # Não esperamos chegar aqui.
    conexao.commit()
    print("ERRO: o banco permitiu um cartão duplicado!")

except sqlite3.IntegrityError:
    # Resultado esperado: o banco bloqueou a duplicidade.
    conexao.rollback()
    print("SUCESSO: o banco impediu o cartão duplicado!")

finally:
    conexao.close()