from decimal import Decimal

from src.persistencia.BD import conectar_banco


class RepositorioDespesas:
    # Salva a configuração de uma despesa recorrente.
    def salvar(self, despesa):
        conexao = conectar_banco()
        try:
            valor_centavos = int(despesa.valor_mensal * 100)
            cursor = conexao.execute(
                """
                INSERT INTO despesas_recorrentes (
                    descricao,
                    valor_mensal_centavos,
                    dia_vencimento,
                    data_inicio,
                    data_fim
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    despesa.descricao,
                    valor_centavos,
                    despesa.dia_vencimento,
                    despesa.data_inicio.isoformat(),
                    (
                        despesa.data_fim.isoformat()
                        if despesa.data_fim is not None
                        else None
                    ),
                ),
            )

            conexao.commit()
            return cursor.lastrowid

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # Lista todas as despesas cadastradas.
    def listar(self):
        conexao = conectar_banco()
        try:
            registros = conexao.execute(
                """
                SELECT
                    id,
                    descricao,
                    valor_mensal_centavos,
                    dia_vencimento,
                    data_inicio,
                    data_fim
                FROM despesas_recorrentes
                ORDER BY descricao, id
                """
            ).fetchall()

            despesas = []

            for registro in registros:
                despesa = dict(registro)

                # Converte centavos em reais.
                despesa["valor_mensal"] = str(
                    Decimal(despesa.pop("valor_mensal_centavos")) / 100
                )

                despesas.append(despesa)

            return despesas
        finally:
            conexao.close()
