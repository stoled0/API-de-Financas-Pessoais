"""
SERVIÇO DO RESUMO FINANCEIRO

Responsabilidade:
Reunir os totais dos cartões e das
despesas recorrentes de um mês.

Não altera compras, cartões ou despesas.
"""

from decimal import Decimal
from src.dominio.contratos_repositorios import ConsultaResumoCartoes, ConsultaCobrancas

class ServicoResumo:
    def __init__(
        self,
        repositorio_resumo: ConsultaResumoCartoes,
        servico_despesas: ConsultaCobrancas
    ):
        self.repositorio_resumo = repositorio_resumo
        self.servico_despesas = servico_despesas

    def consultar_resumo(self, ano: int, mes: int):
        # Valida o período solicitado.
        if not 1 <= ano <= 9999:
            raise ValueError("O ano informado é inválido.")
        if not 1 <= mes <= 12:
            raise ValueError("O mês deve estar entre 1 e 12.")
        
        # Consulta os cartões.
        cartoes = self.repositorio_resumo.consultar_cartoes(
            ano, mes
        )
        # Consulta as despesas recorrentes.
        despesas = self.servico_despesas.consultar_cobrancas(
            ano, mes
        )
        # Soma os valores dos cartões.
        total_cartoes = sum(
            (
                Decimal(cartao["total"])
                for cartao in cartoes
            ),
            Decimal("0")
        )
        # Soma os valores das despesas.
        total_despesas = sum(
            (
                Decimal(despesa["valor"])
                for despesa in despesas
            ),
            Decimal("0")
        )

        # Calcula o total geral.
        total_geral = total_cartoes + total_despesas
        return {
            "ano": ano,
            "mes": mes,
            "cartoes": cartoes,
            "despesas_recorrentes": despesas,
            "total_cartoes": str(total_cartoes),
            "total_despesas": str(total_despesas),
            "total_geral": str(total_geral)
        }