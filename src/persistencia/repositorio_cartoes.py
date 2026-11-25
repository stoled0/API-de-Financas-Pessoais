import sqlite3

from src.persistencia.BD import conectar_banco


class RepositorioCartoes:
    # Salva um cartão e devolve seu ID interno.
    def salvar(self, cartao):
        conexao = conectar_banco()
        try:
            cursor = conexao.execute(
                """
                INSERT INTO cartoes (
                    nome, dia_fechamento, dia_vencimento
                )
                VALUES (?, ?, ?)
                """,
                (cartao.nome, cartao.dia_fechamento, cartao.dia_vencimento),
            )
            conexao.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError as erro:
            conexao.rollback()

            if "idx_cartoes_nome_unico" in str(erro):
                raise ValueError(
                    "Já existe um cartão cadastrado com esse nome."
                ) from erro
            raise
        finally:
            conexao.close()

    # Lista todos os cartões.
    def listar(self):
        conexao = conectar_banco()
        try:
            registros = conexao.execute(
                """
                SELECT id, nome, dia_fechamento, dia_vencimento
                FROM cartoes
                ORDER BY nome
                """
            ).fetchall()
            return [dict(registro) for registro in registros]
        finally:
            conexao.close()

    # Busca um cartão pelo ID interno.
    def buscar_por_id(self, cartao_id):
        conexao = conectar_banco()
        try:
            registro = conexao.execute(
                """
                SELECT id, nome, dia_fechamento, dia_vencimento
                FROM cartoes
                WHERE id = ?
                """,
                (cartao_id,),
            ).fetchone()
            return dict(registro) if registro else None
        finally:
            conexao.close()

    # Busca pelo nome, ignorando maiúsculas e espaços.
    def buscar_por_nome(self, nome):
        conexao = conectar_banco()
        try:
            registro = conexao.execute(
                """
                SELECT id, nome, dia_fechamento, dia_vencimento
                FROM cartoes
                WHERE LOWER(TRIM(nome)) = LOWER(TRIM(?))
                """,
                (nome,),
            ).fetchone()
            return dict(registro) if registro else None
        finally:
            conexao.close()

    # Verifica se o cartão possui compras.
    def possui_compras(self, cartao_id):
        conexao = conectar_banco()
        try:
            registro = conexao.execute(
                """
                SELECT COUNT(*) AS quantidade
                FROM compras
                WHERE cartao_id = ?
                """,
                (cartao_id,),
            ).fetchone()
            return registro["quantidade"] > 0
        finally:
            conexao.close()

    # Atualiza o cartão sem comprometer compras existentes.
    def atualizar(self, cartao_id, cartao):
        conexao = conectar_banco()
        try:
            cursor = conexao.execute(
                """
                UPDATE cartoes
                SET
                    nome = ?,
                    dia_fechamento = ?,
                    dia_vencimento = ?
                WHERE id = ?
                  AND (
                      NOT EXISTS (
                          SELECT 1
                          FROM compras
                          WHERE cartao_id = cartoes.id
                      )
                      OR (
                          dia_fechamento = ?
                          AND dia_vencimento = ?
                      )
                  )
                """,
                (
                    cartao.nome,
                    cartao.dia_fechamento,
                    cartao.dia_vencimento,
                    cartao_id,
                    cartao.dia_fechamento,
                    cartao.dia_vencimento,
                ),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            conexao.rollback()

            if "idx_cartoes_nome_unico" in str(erro):
                raise ValueError(
                    "Já existe um cartão cadastrado com esse nome."
                ) from erro

            raise

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # Exclui apenas cartões sem compras vinculadas.
    def excluir(self, cartao_id):
        conexao = conectar_banco()
        try:
            cursor = conexao.execute(
                """
                DELETE FROM cartoes
                WHERE id = ?
                  AND NOT EXISTS (
                      SELECT 1
                      FROM compras
                      WHERE cartao_id = cartoes.id
                  )
                """,
                (cartao_id,),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
