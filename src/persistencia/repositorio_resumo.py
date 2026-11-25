"""
REPOSITÓRIO DO RESUMO FINANCEIRO

Responsabilidade:
Consultar as parcelas dos cartões que vencem
no mês solicitado.

Não altera nenhuma informação do banco.
"""

from decimal import Decimal

from src.persistencia.BD import conectar_banco


class RepositorioResumo:
    def consultar_cartoes(self, ano: int, mes: int):
        # As parcelas são armazenadas com datas reais. Exemplo: 2026-12-05
        # Por isso, podemos filtrar pelo ano e mês.
        mes_referencia = f"{ano:04d}-{mes:02d}"

        conexao = conectar_banco()
        try:
            registros = conexao.execute(
                """
                SELECT
                    cartoes.id AS cartao_id,
                    cartoes.nome AS nome_cartao,
                    SUM(parcelas.valor_centavos) AS total_centavos

                FROM parcelas
                INNER JOIN compras
                    ON compras.id = parcelas.compra_id
                INNER JOIN cartoes
                    ON cartoes.id = compras.cartao_id
                WHERE SUBSTR(parcelas.vencimento, 1, 7) = ?
                GROUP BY cartoes.id, cartoes.nome
                ORDER BY cartoes.nome
                """,
                (mes_referencia,),
            ).fetchall()

            resultado = []

            for registro in registros:
                total = Decimal(registro["total_centavos"]) / Decimal("100")

                resultado.append(
                    {
                        "cartao_id": registro["cartao_id"],
                        "nome_cartao": registro["nome_cartao"],
                        "total": str(total),
                    }
                )

            return resultado
        finally:
            conexao.close()
