# Importa a função que permite acessar o banco SQLite.
from src.persistencia.BD import conectar_banco

# Abre uma conexão com o banco.
conexao = conectar_banco()

try:
    # Consulta os cartões e conta quantas vezes
    # cada nome aparece, ignorando diferenças
    # entre maiúsculas, minúsculas e espaços nas pontas.
    cursor = conexao.execute(
        """
        SELECT
            LOWER(TRIM(nome)) AS nome_normalizado,
            COUNT(*) AS quantidade
        FROM cartoes
        GROUP BY LOWER(TRIM(nome))
        HAVING COUNT(*) > 1
        """
    )

    # Recupera os nomes duplicados.
    duplicados = cursor.fetchall()

    if not duplicados:
        print("Nenhum nome de cartão duplicado encontrado.")

    else:
        print("CARTÕES COM NOMES DUPLICADOS:\n")

        for grupo in duplicados:

            print(
                f"Nome: {grupo['nome_normalizado']} | "
                f"Quantidade: {grupo['quantidade']}"
            )

        print("\nREGISTROS QUE PRECISAM SER ANALISADOS:\n")

        # Mostra os cartões envolvidos na duplicidade.
        cursor = conexao.execute(
            """
            SELECT
                id,
                nome,
                dia_fechamento,
                dia_vencimento
            FROM cartoes
            WHERE LOWER(TRIM(nome)) IN (
                SELECT LOWER(TRIM(nome))
                FROM cartoes
                GROUP BY LOWER(TRIM(nome))
                HAVING COUNT(*) > 1
            )
            ORDER BY LOWER(TRIM(nome)), id
            """
        )

        for cartao in cursor.fetchall():

            print(
                f"ID: {cartao['id']} | "
                f"Nome: {cartao['nome']} | "
                f"Fechamento: {cartao['dia_fechamento']} | "
                f"Vencimento: {cartao['dia_vencimento']}"
            )

finally:
    # Fecha a conexão com o banco.
    conexao.close()