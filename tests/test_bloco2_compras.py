"""
Testes automatizados do Bloco 2 — Compras Parceladas.

Utilizamos um banco SQLite temporário para não modificar
as compras e os cartões do banco principal.
"""

from datetime import date
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.persistencia import BD
from src.dominio.compra import Compra

# Prepara um banco exclusivo para cada teste.
@pytest.fixture
def ambiente(monkeypatch, tmp_path):

    banco_teste = tmp_path / "compras_teste.db"

    monkeypatch.setattr(
        BD,
        "CAMINHO_BANCO",
        banco_teste
    )
    BD.criar_tabelas()

    from src.api.main import app

    with TestClient(app) as cliente:
        yield cliente

# Cadastra um cartão de teste.
def cadastrar_cartao(cliente):
    resposta = cliente.post(
        "/cartoes",
        json={
            "nome": "Nubank",
            "dia_fechamento": 3,
            "dia_vencimento": 10
        }
    )
    assert resposta.status_code == 201

# Dados padrão de uma compra.
def dados_compra(**alteracoes):

    dados = {
        "nome_cartao": "Nubank",
        "descricao": "Notebook",
        "valor_total": "100.00",
        "data_compra": "2026-11-02",
        "quantidade_parcelas": 3,
        "identificacao_fatura": "LOJA TESTE"
    }

    dados.update(alteracoes)

    return dados

# TESTE 1: Cadastro e cálculo das parcelas.
def test_cadastro_e_parcelamento(ambiente):

    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra()
    )
    assert resposta.status_code == 201

    compra = resposta.json()

    assert compra["nome_cartao"] == "Nubank"
    assert compra["quantidade_parcelas"] == 3
    assert len(compra["parcelas"]) == 3

    valores = [
        Decimal(parcela["valor"])
        for parcela in compra["parcelas"]
    ]

    assert valores == [
        Decimal("33.34"),
        Decimal("33.33"),
        Decimal("33.33")
    ]

    assert sum(valores) == Decimal("100.00")

# TESTE 2: Vencimentos das parcelas.
def test_vencimentos(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra()
    )

    assert resposta.status_code == 201
    datas = [
        parcela["vencimento"]
        for parcela in resposta.json()["parcelas"]
    ]

    assert datas == [
        "2026-11-10",
        "2026-12-10",
        "2027-01-10"
    ]

# TESTE 3: Compra no dia do fechamento.
def test_compra_no_fechamento(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            data_compra="2026-11-03",
            quantidade_parcelas=1
        )
    )

    assert resposta.status_code == 201
    assert (
        resposta.json()["parcelas"][0]["vencimento"]
        == "2026-11-10"
    )

# TESTE 4: Compra após o fechamento.
def test_compra_apos_fechamento(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            data_compra="2026-11-04",
            quantidade_parcelas=1
        )
    )

    assert resposta.status_code == 201
    assert (
        resposta.json()["parcelas"][0]["vencimento"]
        == "2026-12-10"
    )


# TESTE 5: Consulta das compras salvas.
def test_listagem_com_parcelas(ambiente):
    cadastrar_cartao(ambiente)

    ambiente.post(
        "/compras",
        json=dados_compra()
    )

    resposta = ambiente.get("/compras")
    assert resposta.status_code == 200
    compras = resposta.json()

    assert len(compras) == 1
    assert compras[0]["descricao"] == "Notebook"
    assert len(compras[0]["parcelas"]) == 3

    assert Decimal(
        compras[0]["valor_total"]
    ) == Decimal("100.00")


# TESTE 6: Cartão inexistente.
def test_cartao_inexistente(ambiente):
    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            nome_cartao="Cartao Inexistente"
        )
    )

    assert resposta.status_code == 400


# TESTE 7: Descrição obrigatória.
def test_descricao_invalida(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(descricao="   ")
    )

    assert resposta.status_code == 400


# TESTE 8: Valor inválido.
@pytest.mark.parametrize(
    "valor",
    ["0", "-10.00", "abc", "10.999"]
)
def test_valor_invalido(ambiente, valor):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(valor_total=valor)
    )

    assert resposta.status_code == 400


# TESTE 9: Quantidade de parcelas inválida.
@pytest.mark.parametrize(
    "quantidade",
    [0, 49, -1]
)
def test_quantidade_parcelas_invalida(
    ambiente, quantidade
):
    cadastrar_cartao(ambiente)
    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            quantidade_parcelas=quantidade
        )
    )

    assert resposta.status_code == 400

# TESTE 10: Uma única parcela.
def test_compra_a_vista_no_credito(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            valor_total="75.90",
            quantidade_parcelas=1
        )
    )

    assert resposta.status_code == 201
    parcelas = resposta.json()["parcelas"]
    assert len(parcelas) == 1
    assert Decimal(
        parcelas[0]["valor"]
    ) == Decimal("75.90")


# TESTE 11: O banco deve guardar compra e parcelas.
def test_persistencia_sqlite(ambiente):
    cadastrar_cartao(ambiente)
    resposta = ambiente.post(
        "/compras",
        json=dados_compra()
    )

    assert resposta.status_code == 201
    compra_id = resposta.json()["id"]
    conexao = BD.conectar_banco()

    try:
        compra = conexao.execute(
            "SELECT * FROM compras WHERE id = ?",
            (compra_id,)
        ).fetchone()

        parcelas = conexao.execute(
            """
            SELECT *
            FROM parcelas
            WHERE compra_id = ?
            ORDER BY numero
            """,
            (compra_id,)
        ).fetchall()

        assert compra is not None
        assert compra["valor_total_centavos"] == 10000

        assert len(parcelas) == 3

        assert sum(
            parcela["valor_centavos"]
            for parcela in parcelas
        ) == 10000
    finally:
        conexao.close()


# TESTE 12: Uma compra inválida não pode ser salva.
def test_compra_invalida_nao_persiste(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            quantidade_parcelas=49
        )
    )

    assert resposta.status_code == 400
    conexao = BD.conectar_banco()
    try:
        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM compras"
        ).fetchone()[0]

        assert quantidade == 0

    finally:
        conexao.close()

# TESTE 13: Se uma parcela falhar, toda a compra deve ser desfeita pelo SQLite (rollback).
def test_rollback_ao_salvar_parcelas(ambiente):
    from src.persistencia.repositorio_compras import (
        RepositorioCompras
    )

    # Criamos um cartão válido.
    cadastrar_cartao(ambiente)

    # Criamos uma compra válida usando o domínio.
    compra = Compra(
        cartao_id=1,
        descricao="Compra para testar rollback",
        valor_total=Decimal("100.00"),
        data_compra=date(2026, 11, 2),
        quantidade_parcelas=2
    )

    # Simulamos duas parcelas com o mesmo número.
    # O banco possui uma restrição UNIQUE que
    # impede parcelas repetidas na mesma compra.
    parcelas = [
        {
            "numero": 1,
            "valor": Decimal("50.00"),
            "vencimento": date(2026, 11, 10)
        },
        {
            "numero": 1,
            "valor": Decimal("50.00"),
            "vencimento": date(2026, 12, 10)
        }
    ]

    repositorio = RepositorioCompras()

    # Esperamos que o SQLite identifique a duplicidade.
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.salvar(compra, parcelas)

    # Confirma que a compra e suas parcelas
    # não permaneceram salvas no banco.
    conexao = BD.conectar_banco()
    try:
        total_compras = conexao.execute(
            "SELECT COUNT(*) FROM compras"
        ).fetchone()[0]

        total_parcelas = conexao.execute(
            "SELECT COUNT(*) FROM parcelas"
        ).fetchone()[0]

        assert total_compras == 0
        assert total_parcelas == 0

    finally:
        conexao.close()

# TESTE 14: Compra com o máximo de 48 parcelas.
def test_compra_com_48_parcelas(ambiente):
    cadastrar_cartao(ambiente)

    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            valor_total="4800.00",
            quantidade_parcelas=48,
            data_compra="2026-11-02"
        )
    )

    assert resposta.status_code == 201
    parcelas = resposta.json()["parcelas"]
    assert len(parcelas) == 48

    # Primeira parcela em novembro de 2026.
    assert parcelas[0]["vencimento"] == "2026-11-10"

    # Última parcela em outubro de 2030.
    assert parcelas[-1]["vencimento"] == "2030-10-10"

    # Confirma que a soma das parcelas
    # corresponde exatamente ao valor original.
    soma = sum(
        Decimal(parcela["valor"])
        for parcela in parcelas
    )

    assert soma == Decimal("4800.00")

# TESTE 15: Cartão com vencimento no mês seguinte.
def test_vencimento_mes_seguinte(ambiente):
    # Cadastra um cartão com fechamento dia 25
    # e vencimento dia 5.
    resposta_cartao = ambiente.post(
        "/cartoes",
        json={
            "nome": "Inter",
            "dia_fechamento": 25,
            "dia_vencimento": 5
        }
    )
    assert resposta_cartao.status_code == 201
    resposta = ambiente.post(
        "/compras",
        json=dados_compra(
            nome_cartao="Inter",
            data_compra="2026-11-20",
            quantidade_parcelas=2
        )
    )
    assert resposta.status_code == 201
    parcelas = resposta.json()["parcelas"]
    assert parcelas[0]["vencimento"] == "2026-12-05"
    assert parcelas[1]["vencimento"] == "2027-01-05"