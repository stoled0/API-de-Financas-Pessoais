from datetime import date
from decimal import Decimal

class DespesaRecorrente:
    def __init__(
        self,
        descricao: str,
        valor_mensal: Decimal,
        dia_vencimento: int,
        data_inicio: date,
        data_fim: date | None = None
    ):
        # A descrição é obrigatória.
        if not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("A descrição é obrigatória.")

        # O valor precisa ser positivo e ter até duas casas decimais.
        if not isinstance(valor_mensal, Decimal):
            raise ValueError("O valor deve ser do tipo Decimal.")

        if not valor_mensal.is_finite() or valor_mensal <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        if valor_mensal.as_tuple().exponent < -2:
            raise ValueError("O valor deve ter no máximo duas casas decimais.")

        # Todos os meses são tratados como se tivessem dias de 1 a 31.
        if type(dia_vencimento) is not int or not 1 <= dia_vencimento <= 31:
            raise ValueError("O dia de vencimento deve estar entre 1 e 31.")

        # Verifica as datas de início e término.
        if not isinstance(data_inicio, date):
            raise ValueError("A data de início é inválida.")

        if data_fim is not None:
            if not isinstance(data_fim, date) or data_fim < data_inicio:
                raise ValueError("A data de término é inválida.")

        # Guarda os dados da despesa.
        self.descricao = descricao.strip()
        self.valor_mensal = valor_mensal
        self.dia_vencimento = dia_vencimento
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    # Gera uma cobrança por mês no período informado.
    def gerar_cobrancas(self, ano_inicio, mes_inicio, ano_fim, mes_fim):
        cobrancas = []

        # Converte ano e mês em um número para facilitar a repetição.
        primeiro_mes = ano_inicio * 12 + mes_inicio - 1
        ultimo_mes = ano_fim * 12 + mes_fim - 1

        for mes_atual in range(primeiro_mes, ultimo_mes + 1):
            ano = mes_atual // 12
            mes = mes_atual % 12 + 1
            # Usa ano, mês e dia separadamente. Assim, não precisamos criar datas inexistentes.
            vencimento = (
                ano,
                mes,
                self.dia_vencimento
            )
            inicio = (
                self.data_inicio.year,
                self.data_inicio.month,
                self.data_inicio.day
            )
            fim = None
            if self.data_fim is not None:
                fim = (
                    self.data_fim.year,
                    self.data_fim.month,
                    self.data_fim.day
                )

            # Inclui somente cobranças dentro do período de vigência da despesa.
            if vencimento >= inicio and (fim is None or vencimento <= fim):

                cobrancas.append({
                    "descricao": self.descricao,
                    "valor": self.valor_mensal,
                    "ano": ano,
                    "mes": mes,
                    "dia_vencimento": self.dia_vencimento
                })

        return cobrancas