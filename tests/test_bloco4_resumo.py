
"""
TESTES DO BLOCO 4 — RESUMO FINANCEIRO MENSAL

Verificamos:
1. Resumo de um mês sem lançamentos.
2. Soma de parcelas de um mesmo cartão.
3. Soma de vários cartões.
4. Inclusão das despesas recorrentes.
5. Respeito ao mês de vencimento.
6. Ausência de duplicações.
7. Validação de mês e ano.
8. Integração com a API.

Todos os testes utilizam um banco SQLite temporário.
"""

from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from src.persistencia import BD
from src.api import main

from src.aplicacao.servico_cartoes import ServicoCartoes
from src.aplicacao.servico_compras import ServicoCompras
from src.aplicacao.servico_despesas import ServicoDespesas
from src.aplicacao.servico_resumo import ServicoResumo


# ============================================================
# 1. PREPARAÇÃO DO BANCO TEMPORÁRIO
# ============================================================

@pytest.fixture
def ambiente(tmp_path, monkeypatch):

    # Cada teste recebe um banco novo e independente.
    caminho = tmp_path / "teste_resumo.db"

    monkeypatch.setattr(
        BD,
        "CAMINHO_BANCO",
        caminho
    )

    BD.criar_tabelas()

    # Criamos os serviços que já existem no projeto.
    cartoes = ServicoCartoes()
    compras = ServicoCompras()
    despesas = ServicoDespesas()

    resumo = ServicoResumo(
        servico_despesas=despesas
    )

    # A API utiliza os mesmos serviços do teste.
    monkeypatch.setattr(main, "servico_cartoes", cartoes)
    monkeypatch.setattr(main, "servico_compras", compras)
    monkeypatch.setattr(main, "servico_despesas", despesas)
    monkeypatch.setattr(main, "servico_resumo", resumo)

    return {
        "cartoes": cartoes,
        "compras": compras,
        "despesas": despesas,
        "resumo": resumo
    }


@pytest.fixture
def cliente(ambiente):
    return TestClient(main.app)


# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def cadastrar_cartao(servico, nome):

    return servico.cadastrar_cartao(
        nome=nome,
        dia_fechamento=25,
        dia_vencimento=5
    )


def cadastrar_compra(
    servico,
    nome_cartao,
    valor,
    parcelas=1,
    data_compra=date(2026, 11, 20)
):

    return servico.cadastrar_compra(
        nome_cartao=nome_cartao,
        descricao="Compra de teste",
        valor_total=Decimal(valor),
        data_compra=data_compra,
        quantidade_parcelas=parcelas
    )


def cadastrar_despesa(
    servico,
    descricao="Internet",
    valor="120.00",
    dia=10
):

    return servico.cadastrar_despesa(
        descricao=descricao,
        valor_mensal=Decimal(valor),
        dia_vencimento=dia,
        data_inicio=date(2026, 11, 1)
    )


# ============================================================
# 3. TESTES DO RESUMO
# ============================================================

def test_resumo_sem_lancamentos(ambiente):

    resultado = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert resultado["cartoes"] == []
    assert resultado["despesas_recorrentes"] == []

    assert Decimal(resultado["total_cartoes"]) == 0
    assert Decimal(resultado["total_despesas"]) == 0
    assert Decimal(resultado["total_geral"]) == 0


def test_somar_compras_do_mesmo_cartao(ambiente):

    cadastrar_cartao(
        ambiente["cartoes"],
        "Nubank"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "300.00"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "200.00"
    )

    resultado = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert len(resultado["cartoes"]) == 1

    assert Decimal(
        resultado["total_cartoes"]
    ) == Decimal("500.00")


def test_somar_varios_cartoes(ambiente):

    cadastrar_cartao(
        ambiente["cartoes"],
        "Nubank"
    )

    cadastrar_cartao(
        ambiente["cartoes"],
        "Inter"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "300.00"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Inter",
        "200.00"
    )

    resultado = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert len(resultado["cartoes"]) == 2

    assert Decimal(
        resultado["total_cartoes"]
    ) == Decimal("500.00")


def test_incluir_despesas_recorrentes(ambiente):

    cadastrar_despesa(
        ambiente["despesas"],
        "Internet",
        "120.00"
    )

    cadastrar_despesa(
        ambiente["despesas"],
        "Academia",
        "99.90"
    )

    resultado = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert len(
        resultado["despesas_recorrentes"]
    ) == 2

    assert Decimal(
        resultado["total_despesas"]
    ) == Decimal("219.90")


def test_somar_cartoes_e_despesas(ambiente):

    cadastrar_cartao(
        ambiente["cartoes"],
        "Nubank"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "300.00"
    )

    cadastrar_despesa(
        ambiente["despesas"],
        "Internet",
        "120.00"
    )

    resultado = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert Decimal(
        resultado["total_cartoes"]
    ) == Decimal("300.00")

    assert Decimal(
        resultado["total_despesas"]
    ) == Decimal("120.00")

    assert Decimal(
        resultado["total_geral"]
    ) == Decimal("420.00")


def test_parcela_aparece_no_mes_correto(ambiente):

    cadastrar_cartao(
        ambiente["cartoes"],
        "Nubank"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "300.00",
        parcelas=3
    )

    dezembro = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    janeiro = ambiente["resumo"].consultar_resumo(
        2027, 1
    )

    fevereiro = ambiente["resumo"].consultar_resumo(
        2027, 2
    )

    assert Decimal(
        dezembro["total_cartoes"]
    ) == Decimal("100.00")

    assert Decimal(
        janeiro["total_cartoes"]
    ) == Decimal("100.00")

    assert Decimal(
        fevereiro["total_cartoes"]
    ) == Decimal("100.00")


def test_consultar_duas_vezes_nao_duplica(ambiente):

    cadastrar_cartao(
        ambiente["cartoes"],
        "Nubank"
    )

    cadastrar_compra(
        ambiente["compras"],
        "Nubank",
        "100.00"
    )

    primeira = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    segunda = ambiente["resumo"].consultar_resumo(
        2026, 12
    )

    assert primeira == segunda


@pytest.mark.parametrize(
    "ano, mes",
    [
        (2026, 0),
        (2026, 13),
        (0, 12),
        (10000, 12)
    ]
)
def test_rejeitar_periodo_invalido(
    ambiente,
    ano,
    mes
):

    with pytest.raises(ValueError):
        ambiente["resumo"].consultar_resumo(
            ano, mes
        )


# ============================================================
# 4. TESTES DE INTEGRAÇÃO COM A API
# ============================================================

def test_api_consultar_resumo(cliente):

    resposta = cliente.get(
        "/resumo/2026/12"
    )

    assert resposta.status_code == 200

    dados = resposta.json()

    assert dados["ano"] == 2026
    assert dados["mes"] == 12
    assert Decimal(dados["total_geral"]) == 0


def test_api_rejeitar_mes_invalido(cliente):

    resposta = cliente.get(
        "/resumo/2026/13"
    )

    assert resposta.status_code == 400