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