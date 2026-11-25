from datetime import date
from decimal import Decimal


# Representa uma compra realizada no cartão de crédito.
class Compra:
    VALOR_MINIMO_PARCELA = Decimal("0.01")

    def __init__(
        self,
        cartao_id: int,
        descricao: str,
        valor_total: Decimal,
        data_compra: date,
        quantidade_parcelas: int,
        identificacao_fatura: str = "",
    ):
        # Valida os dados da compra.
        self._validar_cartao(cartao_id)
        self._validar_descricao(descricao)
        self._validar_valor(valor_total)
        self._validar_data(data_compra)
        self._validar_quantidade_parcelas(quantidade_parcelas)
        self._validar_identificacao(identificacao_fatura)

        self._validar_valor_minimo_parcela(valor_total, quantidade_parcelas)

        # Guarda os dados após a validação.
        self.cartao_id = cartao_id
        self.descricao = descricao.strip()
        self.valor_total = valor_total
        self.data_compra = data_compra
        self.quantidade_parcelas = quantidade_parcelas
        self.identificacao_fatura = identificacao_fatura.strip()

    # REGRA 1: Valida o identificador do cartão.
    def _validar_cartao(self, cartao_id):
        if type(cartao_id) is not int or cartao_id <= 0:
            raise ValueError("O cartão informado é inválido.")

    # REGRA 2: A descrição é obrigatória.
    def _validar_descricao(self, descricao):
        if not isinstance(descricao, str) or descricao.strip() == "":
            raise ValueError("A descrição da compra é obrigatória.")

    # REGRAS 3 e 4: Valida o valor total.
    def _validar_valor(self, valor_total):
        if not isinstance(valor_total, Decimal):
            raise ValueError("O valor total deve ser do tipo Decimal.")

        if not valor_total.is_finite() or valor_total <= 0:
            raise ValueError("O valor total deve ser maior que zero.")

        if valor_total.as_tuple().exponent < -2:
            raise ValueError(
                "O valor total deve possuir no máximo duas casas decimais."
            )

    # REGRA 5: Valida a data da compra.
    def _validar_data(self, data_compra):
        if not isinstance(data_compra, date):
            raise ValueError("A data da compra é inválida.")

    # REGRA 6: Permite compras de 1 a 48 parcelas.
    def _validar_quantidade_parcelas(self, quantidade_parcelas):
        if (
            type(quantidade_parcelas) is not int
            or quantidade_parcelas < 1
            or quantidade_parcelas > 48
        ):
            raise ValueError("A quantidade de parcelas deve estar entre 1 e 48.")

    # REGRA 7: Valida a identificação na fatura.
    def _validar_identificacao(self, identificacao_fatura):
        if not isinstance(identificacao_fatura, str):
            raise ValueError("A identificação na fatura deve ser um texto.")

    # REGRA 8: Garante o valor mínimo de cada parcela.
    def _validar_valor_minimo_parcela(self, valor_total, quantidade_parcelas):
        valor_minimo_total = self.VALOR_MINIMO_PARCELA * quantidade_parcelas

        if valor_total < valor_minimo_total:
            raise ValueError("Cada parcela deve possuir valor mínimo de R$ 0,01.")

    # Calcula o valor de cada parcela.
    def calcular_parcelas(self):

        # PASSO 1: Converter o valor total para centavos.
        valor_em_centavos = int(self.valor_total * 100)

        # PASSO 2: Calcular o valor básico de cada parcela.
        valor_base = valor_em_centavos // self.quantidade_parcelas

        # PASSO 3: Descobrir quantos centavos sobraram.
        centavos_restantes = valor_em_centavos % self.quantidade_parcelas

        # PASSO 4: Criar a lista de parcelas.
        parcelas = []

        # PASSO 5: Gerar cada parcela.
        for numero in range(self.quantidade_parcelas):
            valor_parcela = valor_base

            # Distribui os centavos restantes.
            if numero < centavos_restantes:
                valor_parcela += 1

            # Converte o valor novamente para reais.
            valor_em_reais = Decimal(valor_parcela) / Decimal("100")

            parcelas.append(valor_em_reais)

        # PASSO 6: Devolver as parcelas calculadas.
        return parcelas
