# Importa a função que abre a conexão com o SQLite.
from src.persistencia.BD import conectar_banco

# Responsável por salvar compras e suas parcelas.
class RepositorioCompras:
    # Recebe uma compra validada e suas parcelas calculadas.
    def salvar(self, compra, parcelas):
        # Abre uma conexão com o banco de dados.
        conexao = conectar_banco()

        try:
            # PASSO 1: Converter o valor total para centavos.
            valor_total_centavos = int(
                compra.valor_total * 100
            )

            # PASSO 2: Salvar os dados gerais da compra.
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

            # Recupera o identificador da compra criada.
            compra_id = cursor.lastrowid

            # PASSO 3: Salvar cada parcela da compra.
            for parcela in parcelas:
                # Converte o valor da parcela para centavos.
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

            # PASSO 4: Confirmar todas as operações.
            # O commit só acontece depois que a compra e todas as parcelas foram salvas.
            conexao.commit()

            # Devolve o ID da compra cadastrada.
            return compra_id

        except Exception:
            # Se alguma operação falhar, desfaz
            # todas as alterações desta transação.
            conexao.rollback()

            # Repassa o erro para a camada responsável
            # por tratá-lo.
            raise

        finally:
            # Fecha a conexão, com sucesso ou erro.
            conexao.close()