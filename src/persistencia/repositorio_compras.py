from decimal import Decimal
from src.persistencia.BD import conectar_banco

class RepositorioCompras:
    # Salva uma compra e todas as suas parcelas.
    def salvar(self, compra, parcelas):
        conexao = conectar_banco()
        try:
            # O banco guarda valores monetários em centavos.
            valor_total_centavos = int(
                compra.valor_total * 100
            )
            # Primeiro, salva a compra.
            cursor = conexao.execute(
                """
                INSERT INTO compras (
                    cartao_id,
                    descricao,
                    identificacao_fatura,
                    valor_total_centavos,
                    data_compra,
                    quantidade_parcelas
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    compra.cartao_id,
                    compra.descricao,
                    compra.identificacao_fatura,
                    valor_total_centavos,
                    compra.data_compra.isoformat(),
                    compra.quantidade_parcelas
                )
            )
            # Recupera o ID criado pelo SQLite.
            compra_id = cursor.lastrowid

            # Salva cada parcela vinculada à compra.
            for parcela in parcelas:
                valor_centavos = int(
                    parcela["valor"] * 100
                )
                conexao.execute(
                    """
                    INSERT INTO parcelas (
                        compra_id,
                        numero,
                        valor_centavos,
                        vencimento
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        compra_id,
                        parcela["numero"],
                        valor_centavos,
                        parcela["vencimento"].isoformat()
                    )
                )

            # Confirma a compra e todas as parcelas juntas.
            conexao.commit()
            return compra_id
        except Exception:
            # Se alguma parcela falhar, desfaz tudo.
            conexao.rollback()
            raise
        finally:
            conexao.close()

    # Lista as compras com o nome do cartão.
    def listar(self):
        conexao = conectar_banco()
        try:
            registros = conexao.execute(
                """
                SELECT
                    compras.id,
                    cartoes.nome AS nome_cartao,
                    compras.descricao,
                    compras.identificacao_fatura,
                    compras.valor_total_centavos,
                    compras.data_compra,
                    compras.quantidade_parcelas
                FROM compras
                INNER JOIN cartoes
                    ON cartoes.id = compras.cartao_id
                ORDER BY compras.data_compra DESC,
                         compras.id DESC
                """
            ).fetchall()
            resultado = []

            for registro in registros:

                compra = dict(registro)

                # Recupera as parcelas desta compra.
                parcelas = conexao.execute(
                    """
                    SELECT
                        numero,
                        valor_centavos,
                        vencimento
                    FROM parcelas
                    WHERE compra_id = ?
                    ORDER BY numero
                    """,
                    (compra["id"],)
                ).fetchall()

                # Converte centavos para valores em reais.
                compra["valor_total"] = str(
                    Decimal(
                        compra.pop("valor_total_centavos")
                    ) / 100
                )

                compra["parcelas"] = [
                    {
                        "numero": parcela["numero"],
                        "valor": str(
                            Decimal(
                                parcela["valor_centavos"]
                            ) / 100
                        ),
                        "vencimento": parcela["vencimento"]
                    }
                    for parcela in parcelas
                ]
                resultado.append(compra)
            return resultado
        finally:
            conexao.close()