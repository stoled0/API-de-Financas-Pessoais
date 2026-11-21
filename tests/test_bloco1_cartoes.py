"""
Testes automatizados do Bloco 1.
Executar:
python -m pytest tests/test_bloco1_cartoes.py -v
Os testes NÃO utilizam o financas.db principal.
"""

import sqlite3
import pytest
from fastapi.testclient import TestClient
from src.dominio.cartao import Cartao
from src.persistencia import BD

@pytest.fixture
def ambiente(monkeypatch, tmp_path):
    """
    Prepara um banco SQLite exclusivo para cada teste.

    monkeypatch altera temporariamente o caminho do banco.
    tmp_path cria uma pasta temporária.
    """

    banco_teste = tmp_path / "cartoes_teste.db"

    monkeypatch.setattr(
        BD,
        "CAMINHO_BANCO",
        banco_teste
    )

    # Cria as tabelas e o índice de nomes únicos.
    BD.criar_tabelas()

    # Importa a API após configurar o banco de teste.
    from src.api.main import app

    with TestClient(app) as cliente:
        yield cliente


def cadastrar(cliente, nome="Cartao Teste",
              fechamento=5, vencimento=12):
    """Facilita o cadastro durante os testes."""

    return cliente.post(
        "/cartoes",
        json={
            "nome": nome,
            "dia_fechamento": fechamento,
            "dia_vencimento": vencimento
        }
    )


def vincular_compra(nome_cartao):
    """
    Insere uma compra fictícia no banco temporário.

    Isso permite testar as proteções dos cartões
    sem depender da API de compras do Bloco 2.
    """

    conexao = BD.conectar_banco()

    try:
        cartao = conexao.execute(
            """
            SELECT id
            FROM cartoes
            WHERE nome = ?
            """,
            (nome_cartao,)
        ).fetchone()

        conexao.execute(
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
                cartao["id"],
                "Compra fictícia",
                "TESTE",
                10000,
                "2026-11-21",
                1
            )
        )

        conexao.commit()

    finally:
        conexao.close()


# TESTE 1: Validações do domínio.
@pytest.mark.parametrize(
    "nome, fechamento, vencimento",
    [
        ("", 5, 12),
        ("   ", 5, 12),
        ("Teste", 0, 12),
        ("Teste", 29, 12),
        ("Teste", 5, 0),
        ("Teste", 5, 29),
        ("Teste", "cinco", 12),
        ("Teste", 5, "doze"),
        (None, 5, 12),
    ]
)
def test_dominio_rejeita_dados_invalidos(
    nome, fechamento, vencimento
):
    with pytest.raises(ValueError):
        Cartao(nome, fechamento, vencimento)


# TESTE 2: Cadastro, listagem e busca.
def test_cadastro_listagem_e_consulta(ambiente):
    resposta = cadastrar(ambiente)

    assert resposta.status_code == 201

    cartao = resposta.json()

    assert cartao["nome"] == "Cartao Teste"
    assert cartao["dia_fechamento"] == 5

    listagem = ambiente.get("/cartoes")

    assert listagem.status_code == 200
    assert len(listagem.json()) == 1

    consulta = ambiente.get("/cartoes/cartao teste")

    assert consulta.status_code == 200
    assert consulta.json()["id"] == cartao["id"]


# TESTE 3: Impede nomes duplicados.
def test_nome_duplicado(ambiente):
    assert cadastrar(ambiente, "Nubank").status_code == 201

    duplicado = cadastrar(ambiente, " NUBANK ")

    assert duplicado.status_code == 400
    assert "Já existe" in duplicado.json()["detail"]


# TESTE 4: Edição completa sem compras.
def test_edicao_sem_compras(ambiente):
    cadastrar(ambiente)

    resposta = ambiente.patch(
        "/cartoes/Cartao Teste",
        json={
            "nome": "Cartao Atualizado",
            "dia_fechamento": 8,
            "dia_vencimento": 15
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Cartao Atualizado"
    assert resposta.json()["dia_fechamento"] == 8
    assert resposta.json()["dia_vencimento"] == 15


# TESTE 5: Não permite renomear para nome existente.
def test_edicao_com_nome_duplicado(ambiente):
    cadastrar(ambiente, "Nubank")
    cadastrar(ambiente, "Inter")

    resposta = ambiente.patch(
        "/cartoes/Inter",
        json={"nome": " NUBANK "}
    )

    assert resposta.status_code == 400

    # Confirma que o nome original foi preservado.
    assert ambiente.get("/cartoes/Inter").status_code == 200


# TESTE 6: Cartão com compras pode mudar de nome.
def test_renomear_cartao_com_compras(ambiente):
    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    resposta = ambiente.patch(
        "/cartoes/Nubank",
        json={"nome": "Nubank - Sarah"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Nubank - Sarah"


# TESTE 7: Cartão com compras não muda vencimento.
def test_bloquear_edicao_com_compras(ambiente):
    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    resposta = ambiente.patch(
        "/cartoes/Nubank",
        json={"dia_vencimento": 20}
    )

    assert resposta.status_code == 400

    consulta = ambiente.get("/cartoes/Nubank")

    assert consulta.json()["dia_vencimento"] == 12


# TESTE 8: Cartão com compras não pode ser excluído.
def test_bloquear_exclusao_com_compras(ambiente):
    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    resposta = ambiente.delete("/cartoes/Nubank")

    assert resposta.status_code == 400

    # O cartão deve continuar existindo.
    assert ambiente.get("/cartoes/Nubank").status_code == 200


# TESTE 9: Exclusão de cartão sem compras.
def test_exclusao_permitida(ambiente):
    cadastrar(ambiente)

    resposta = ambiente.delete("/cartoes/Cartao Teste")

    assert resposta.status_code == 200

    consulta = ambiente.get("/cartoes/Cartao Teste")

    assert consulta.status_code == 404


# TESTE 10: Cartão inexistente.
def test_cartao_inexistente(ambiente):
    assert ambiente.get(
        "/cartoes/Inexistente"
    ).status_code == 404

    assert ambiente.patch(
        "/cartoes/Inexistente",
        json={"nome": "Novo"}
    ).status_code == 404

    assert ambiente.delete(
        "/cartoes/Inexistente"
    ).status_code == 404


# TESTE 11: Validação de dados recebidos pela API.
def test_dados_invalidos_na_api(ambiente):
    resposta = cadastrar(
        ambiente,
        nome="Teste",
        fechamento="texto"
    )

    assert resposta.status_code == 422

    resposta = cadastrar(
        ambiente,
        nome="",
        fechamento=5
    )

    assert resposta.status_code == 400


# TESTE 12: Banco impede nomes duplicados.
def test_indice_unico_sqlite(ambiente):
    cadastrar(ambiente, "Nubank")

    conexao = BD.conectar_banco()

    try:
        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                """
                INSERT INTO cartoes (
                    nome,
                    dia_fechamento,
                    dia_vencimento
                )
                VALUES (?, ?, ?)
                """,
                (" nubank ", 5, 12)
            )

    finally:
        conexao.rollback()
        conexao.close()


# TESTE 13: O Repository impede excluir cartão com compras.
def test_repositorio_bloqueia_exclusao_com_compras(ambiente):
    from src.persistencia.repositorio_cartoes import RepositorioCartoes

    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    repositorio = RepositorioCartoes()
    cartao = repositorio.buscar_por_nome("Nubank")

    # Tenta excluir diretamente pelo Repository,
    # sem passar pelo serviço ou pela API.
    excluido = repositorio.excluir(cartao["id"])

    assert excluido is False
    assert repositorio.buscar_por_nome("Nubank") is not None


# TESTE 14: O Repository impede alterar vencimento
# de um cartão com compras vinculadas.
def test_repositorio_bloqueia_edicao_com_compras(ambiente):
    from src.persistencia.repositorio_cartoes import RepositorioCartoes

    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    repositorio = RepositorioCartoes()
    cartao_atual = repositorio.buscar_por_nome("Nubank")

    cartao_alterado = Cartao(
        nome="Nubank",
        dia_fechamento=5,
        dia_vencimento=20
    )

    atualizado = repositorio.atualizar(
        cartao_atual["id"],
        cartao_alterado
    )

    assert atualizado is False

    # O vencimento original precisa continuar preservado.
    cartao_depois = repositorio.buscar_por_nome("Nubank")
    assert cartao_depois["dia_vencimento"] == 12


# TESTE 15: O SQLite impede excluir cartão com compras
# por causa da chave estrangeira.
def test_sqlite_protege_relacionamento_compras(ambiente):
    cadastrar(ambiente, "Nubank")
    vincular_compra("Nubank")

    conexao = BD.conectar_banco()

    try:
        cartao = conexao.execute(
            "SELECT id FROM cartoes WHERE nome = ?",
            ("Nubank",)
        ).fetchone()

        # Confirma que a proteção de chave estrangeira
        # está ativada nesta conexão.
        ativado = conexao.execute(
            "PRAGMA foreign_keys"
        ).fetchone()[0]

        assert ativado == 1

        # Tenta excluir diretamente pelo SQL.
        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                "DELETE FROM cartoes WHERE id = ?",
                (cartao["id"],)
            )

    finally:
        conexao.rollback()
        conexao.close()


# TESTE 16: Uma tentativa de edição inválida
# não pode alterar os dados originais.
def test_edicao_invalida_preserva_dados(ambiente):
    cadastrar(ambiente, "Nubank", 5, 12)

    resposta = ambiente.patch(
        "/cartoes/Nubank",
        json={
            "nome": "Novo Nome",
            "dia_fechamento": 30
        }
    )

    assert resposta.status_code == 400

    # Confirma que nenhum campo foi alterado.
    consulta = ambiente.get("/cartoes/Nubank")

    assert consulta.status_code == 200
    assert consulta.json()["nome"] == "Nubank"
    assert consulta.json()["dia_fechamento"] == 5
    assert consulta.json()["dia_vencimento"] == 12