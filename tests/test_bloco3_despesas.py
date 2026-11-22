"""
TESTES DO BLOCO 3 — DESPESAS RECORRENTES

Testamos:
1. Validações do domínio.
2. Geração das cobranças mensais.
3. Persistência no SQLite.
4. Integração com a API FastAPI.

Os testes usam um banco temporário.
Não alteram o financas.db principal.
"""

from datetime import date
from decimal import Decimal
import sqlite3
import pytest
from fastapi.testclient import TestClient
from src.dominio.despesa_recorrente import DespesaRecorrente
from src.aplicacao.servico_despesas import ServicoDespesas
from src.persistencia import BD
from src.api import main
from src.persistencia.repositorio_despesas import RepositorioDespesas

# ============================================================
# 1. BANCO TEMPORÁRIO PARA OS TESTES
# ============================================================

@pytest.fixture
def banco_temporario(tmp_path, monkeypatch):

    # Substitui o caminho do banco somente durante o teste.
    caminho = tmp_path / "teste_despesas.db"

    monkeypatch.setattr(BD, "CAMINHO_BANCO", caminho)

    # Cria as tabelas no banco temporário.
    BD.criar_tabelas()

    # Cria um serviço que utiliza esse banco.
    servico = ServicoDespesas(RepositorioDespesas())

    # Faz as rotas da API usarem o serviço de teste.
    monkeypatch.setattr(
        main,
        "servico_despesas",
        servico
    )

    return caminho

@pytest.fixture
def cliente(banco_temporario):
    return TestClient(main.app)

# ============================================================
# 2. TESTES DAS REGRAS DE NEGÓCIO
# ============================================================

def criar_despesa(
    descricao="Internet",
    valor=Decimal("120.00"),
    dia=10,
    inicio=date(2026, 11, 1),
    fim=None
):
    return DespesaRecorrente(
        descricao=descricao,
        valor_mensal=valor,
        dia_vencimento=dia,
        data_inicio=inicio,
        data_fim=fim
    )

def test_criar_despesa_valida():
    despesa = criar_despesa()

    assert despesa.descricao == "Internet"
    assert despesa.valor_mensal == Decimal("120.00")
    assert despesa.dia_vencimento == 10

@pytest.mark.parametrize(
    "descricao",
    ["", "   ", None]
)
def test_rejeitar_descricao_invalida(descricao):

    with pytest.raises(ValueError):
        criar_despesa(descricao=descricao)

@pytest.mark.parametrize(
    "valor",
    [
        Decimal("0"),
        Decimal("-10"),
        Decimal("10.999"),
        Decimal("NaN")
    ]
)
def test_rejeitar_valor_invalido(valor):

    with pytest.raises(ValueError):
        criar_despesa(valor=valor)

@pytest.mark.parametrize(
    "dia",
    [0, 32, -1, 10.5, True]
)
def test_rejeitar_dia_invalido(dia):

    with pytest.raises(ValueError):
        criar_despesa(dia=dia)

def test_rejeitar_data_fim_anterior_ao_inicio():

    with pytest.raises(ValueError):
        criar_despesa(
            inicio=date(2026, 11, 10),
            fim=date(2026, 11, 1)
        )

# ============================================================
# 3. TESTES DAS COBRANÇAS
# ============================================================
def test_gerar_uma_cobranca_por_mes():
    despesa = criar_despesa()
    cobrancas = despesa.gerar_cobrancas(
        2026, 11, 2027, 1
    )
    assert len(cobrancas) == 3
    assert [
        (c["ano"], c["mes"])
        for c in cobrancas
    ] == [
        (2026, 11),
        (2026, 12),
        (2027, 1)
    ]

def test_todos_os_meses_aceitam_dia_31():
    despesa = criar_despesa(dia=31)
    cobrancas = despesa.gerar_cobrancas(
        2027, 1, 2027, 3
    )
    assert len(cobrancas) == 3
    assert all(
        c["dia_vencimento"] == 31
        for c in cobrancas
    )


def test_primeira_cobranca_nao_antecede_inicio():
    despesa = criar_despesa(
        dia=10,
        inicio=date(2026, 11, 15)
    )
    cobrancas = despesa.gerar_cobrancas(
        2026, 11, 2026, 12
    )
    assert len(cobrancas) == 1
    assert cobrancas[0]["mes"] == 12

def test_respeitar_data_de_termino():
    despesa = criar_despesa(
        fim=date(2026, 12, 15)
    )
    cobrancas = despesa.gerar_cobrancas(
        2026, 11, 2027, 2
    )
    assert len(cobrancas) == 2

# ============================================================
# 4. TESTES DO BANCO DE DADOS
# ============================================================
def test_salvar_e_listar_despesa(banco_temporario):
    servico = ServicoDespesas(RepositorioDespesas())
    cadastro = servico.cadastrar_despesa(
        descricao="Academia",
        valor_mensal=Decimal("99.90"),
        dia_vencimento=5,
        data_inicio=date(2026, 11, 1)
    )
    despesas = servico.listar_despesas()

    assert cadastro["id"] > 0
    assert len(despesas) == 1
    assert despesas[0]["descricao"] == "Academia"
    assert Decimal(despesas[0]["valor_mensal"]) == Decimal("99.90")

def test_cobrancas_nao_duplicam_no_banco(banco_temporario):
    servico = ServicoDespesas(RepositorioDespesas())
    servico.cadastrar_despesa(
        descricao="Internet",
        valor_mensal=Decimal("120.00"),
        dia_vencimento=10,
        data_inicio=date(2026, 11, 1)
    )
    primeira_consulta = servico.consultar_cobrancas(
        2026, 12
    )
    segunda_consulta = servico.consultar_cobrancas(
        2026, 12
    )
    assert primeira_consulta == segunda_consulta

    # Confirma que existe somente um cadastro no banco.
    conexao = sqlite3.connect(banco_temporario)
    try:
        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM despesas_recorrentes"
        ).fetchone()[0]

        assert quantidade == 1
    finally:
        conexao.close()

# ============================================================
# 5. TESTES DE INTEGRAÇÃO COM A API
# ============================================================
def test_api_cadastrar_e_consultar_despesa(cliente):
    resposta = cliente.post(
        "/despesas",
        json={
            "descricao": "Internet",
            "valor_mensal": "120.00",
            "dia_vencimento": 10,
            "data_inicio": "2026-11-01",
            "data_fim": None
        }
    )
    assert resposta.status_code == 201
    resposta_listagem = cliente.get("/despesas")
    assert resposta_listagem.status_code == 200
    assert len(resposta_listagem.json()) == 1

    resposta_cobrancas = cliente.get(
        "/despesas/cobrancas/2026/12"
    )

    assert resposta_cobrancas.status_code == 200
    cobrancas = resposta_cobrancas.json()
    assert len(cobrancas) == 1
    assert cobrancas[0]["descricao"] == "Internet"
    assert Decimal(cobrancas[0]["valor"]) == Decimal("120.00")

def test_api_rejeitar_valor_negativo(cliente):
    resposta = cliente.post(
        "/despesas",
        json={
            "descricao": "Internet",
            "valor_mensal": "-50.00",
            "dia_vencimento": 10,
            "data_inicio": "2026-11-01"
        }
    )

    assert resposta.status_code == 400

def test_api_rejeitar_mes_invalido(cliente):
    resposta = cliente.get(
        "/despesas/cobrancas/2026/13"
    )
    assert resposta.status_code == 400