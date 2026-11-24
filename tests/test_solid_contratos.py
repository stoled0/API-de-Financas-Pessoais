"""Testes para demonstrar DIP e ISP."""

from datetime import date
from decimal import Decimal
from src.aplicacao.servico_compras import ServicoCompras

class CartoesSomenteConsulta:
    """Oferece apenas a consulta de cartões."""

    def buscar_por_nome(self, nome):
        if nome != "Nubank":
            return None

        return {
            "id": 1,
            "nome": "Nubank",
            "dia_fechamento": 20,
            "dia_vencimento": 10
        }

class ComprasEmMemoria:
    """Armazena compras sem utilizar SQLite."""
    def __init__(self):
        self.registros = []
    def salvar(self, compra, parcelas):
        self.registros.append((compra, parcelas))
        return len(self.registros)
    def listar(self):
        return [
            compra.descricao
            for compra, _ in self.registros
        ]

def test_contrato_de_consulta_de_cartoes_e_pequeno():
    consulta = CartoesSomenteConsulta()
    assert callable(consulta.buscar_por_nome)
    assert not hasattr(consulta, "excluir")
    assert not hasattr(consulta, "salvar")

def test_servico_compras_aceita_repositorios_sem_sqlite():
    compras = ComprasEmMemoria()
    servico = ServicoCompras(
        compras,
        CartoesSomenteConsulta()
    )
    resultado = servico.cadastrar_compra(
        nome_cartao="Nubank",
        descricao="Livro",
        valor_total=Decimal("100.00"),
        data_compra=date(2026, 11, 19),
        quantidade_parcelas=3
    )
    assert resultado["id"] == 1
    assert [
        parcela["valor"]
        for parcela in compras.registros[0][1]
    ] == [
        Decimal("33.34"),
        Decimal("33.33"),
        Decimal("33.33")
    ]
    assert servico.listar_compras() == ["Livro"]

def test_factory_method_cria_servicos():
    from src.aplicacao.fabrica_servicos import FabricaSQLite

    fabrica = FabricaSQLite()
    servicos = fabrica.criar_servicos()

    assert set(servicos) == {
        "cartoes",
        "compras",
        "despesas",
        "resumo"
    }

    assert servicos["compras"].repositorio_cartoes is (
        servicos["cartoes"].repositorio
    )

    assert servicos["resumo"].servico_despesas is (
        servicos["despesas"]
    )


def test_adapter_cadastro_compra():
    from datetime import date
    from decimal import Decimal
    from types import SimpleNamespace

    from src.api.adaptador_cadastro_compra import (
        AdaptadorCadastroCompra
    )

    class ServicoFalso:
        def cadastrar_compra(self, **dados):
            return dados

    dados_api = SimpleNamespace(
        nome_cartao="Nubank",
        descricao="Notebook",
        valor_total="1500.50",
        data_compra=date(2026, 11, 10),
        quantidade_parcelas=3,
        identificacao_fatura="LOJA TESTE"
    )

    adaptador = AdaptadorCadastroCompra(
        ServicoFalso()
    )

    resultado = adaptador.cadastrar(dados_api)

    assert resultado["valor_total"] == Decimal("1500.50")
    assert resultado["nome_cartao"] == "Nubank"
    assert resultado["quantidade_parcelas"] == 3

def test_template_method_geracao_parcelas():
    from datetime import date
    from decimal import Decimal

    from src.dominio.gerador_parcelas import GeradorParcelas
    from src.dominio.compra import Compra

    etapas = []

    class GeradorTeste(GeradorParcelas):

        def calcular_valores(self, compra):
            etapas.append("valores")

            return [
                Decimal("50.00"),
                Decimal("50.00")
            ]

        def calcular_vencimentos(
            self, compra, dia_fechamento, dia_vencimento
        ):
            etapas.append("vencimentos")

            return [
                date(2026, 12, 10),
                date(2027, 1, 10)
            ]

    compra = Compra(
        cartao_id=1,
        descricao="Compra teste",
        valor_total=Decimal("100.00"),
        data_compra=date(2026, 11, 15),
        quantidade_parcelas=2
    )

    gerador = GeradorTeste()

    parcelas = gerador.gerar(
        compra,
        dia_fechamento=5,
        dia_vencimento=10
    )

    assert etapas == ["valores", "vencimentos"]
    assert len(parcelas) == 2
    assert parcelas[0]["valor"] == Decimal("50.00")
    assert parcelas[0]["vencimento"] == date(2026, 12, 10)
    assert parcelas[1]["vencimento"] == date(2027, 1, 10)
