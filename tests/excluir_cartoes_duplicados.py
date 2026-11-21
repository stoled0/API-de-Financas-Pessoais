# Importa a função de conexão com o SQLite.
from src.persistencia.BD import conectar_banco

# Abre a conexão com o banco de dados.
conexao = conectar_banco()

try:
    # IDs dos cartões duplicados que queremos excluir.
    ids_excluir = (5, 5)

    # PASSO 1: Verificar se existem compras vinculadas.
    cursor = conexao.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM compras
        WHERE cartao_id IN (?, ?)
        """,
        ids_excluir
    )

    quantidade_compras = cursor.fetchone()["quantidade"]

    if quantidade_compras > 0:
        print(
            "Exclusão cancelada: existem "
            f"{quantidade_compras} compras vinculadas "
            "aos cartões 2 e 3."
        )

    else:
        # PASSO 2: Excluir somente os cartões duplicados.
        cursor = conexao.execute(
            """
            DELETE FROM cartoes
            WHERE id IN (?, ?)
              AND LOWER(TRIM(nome)) = 'nubank'
            """,
            ids_excluir
        )

        quantidade_excluida = cursor.rowcount

        # PASSO 3: Confirmar a exclusão.
        conexao.commit()

        print(
            f"{quantidade_excluida} cartões "
            "duplicados excluídos com sucesso!"
        )

except Exception:
    # Desfaz alterações caso ocorra algum erro.
    conexao.rollback()
    raise

finally:
    # Fecha a conexão.
    conexao.close()