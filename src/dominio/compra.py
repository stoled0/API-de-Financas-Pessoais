# Importa o tipo date, utilizado para representar datas.
from datetime import date

# Importa Decimal para trabalhar com valores monetários.
# Ele evita problemas de precisão comuns com números decimais.
from decimal import Decimal

# Representa uma compra realizada no cartão de crédito.
class Compra:
    def __init__(
        self,
        cartao_id: int,
        descricao: str,
        valor_total: Decimal,
        data_compra: date,
        quantidade_parcelas: int,
        identificacao_fatura: str = ""
    ):

        # REGRA 1: O cartão deve possuir um identificador válido.
        if type(cartao_id) is not int or cartao_id <= 0:
            raise ValueError("O cartão informado é inválido.")

        # REGRA 2: A descrição da compra é obrigatória.
        if not isinstance(descricao, str) or descricao.strip() == "":
            raise ValueError("A descrição da compra é obrigatória.")

        # REGRA 3: O valor da compra deve ser maior que zero.
        if not isinstance(valor_total, Decimal):
            raise ValueError("O valor total deve ser do tipo Decimal.")

        if not valor_total.is_finite() or valor_total <= 0:
            raise ValueError("O valor total deve ser maior que zero.")

        # REGRA 4: O valor deve possuir no máximo duas casas decimais.
        if valor_total.as_tuple().exponent < -2:
            raise ValueError(
                "O valor total deve possuir no máximo duas casas decimais."
            )

        # REGRA 5: A data deve ser uma data válida.
        if not isinstance(data_compra, date):
            raise ValueError("A data da compra é inválida.")

        # REGRA 6: A compra pode ter de 1 a 48 parcelas.
        if (
            type(quantidade_parcelas) is not int
            or quantidade_parcelas < 1
            or quantidade_parcelas > 48
        ):
            raise ValueError(
                "A quantidade de parcelas deve estar entre 1 e 48."
            )

        # REGRA 7: A identificação na fatura é opcional,
        # mas, quando informada, deve ser um texto.
        if not isinstance(identificacao_fatura, str):
            raise ValueError(
                "A identificação na fatura deve ser um texto."
            )

        # Guarda os dados da compra após a validação.
        self.cartao_id = cartao_id
        self.descricao = descricao.strip()
        self.valor_total = valor_total
        self.data_compra = data_compra
        self.quantidade_parcelas = quantidade_parcelas
        self.identificacao_fatura = identificacao_fatura.strip()


    # Calcula o valor de cada parcela da compra.
    # Exemplo: Compra de R$ 100,00 dividida em 3 vezes.
    # Resultado: [33.34, 33.33, 33.33]
    def calcular_parcelas(self):

        # PASSO 1: Converter o valor total para centavos.
        # Exemplo: R$ 100,00 se transforma em 10000 centavos.
        valor_em_centavos = int(self.valor_total * 100)

        # PASSO 2: Calcular o valor básico de cada parcela.
        # Exemplo: 10000 // 3 = 3333.
        valor_base = valor_em_centavos // self.quantidade_parcelas

        # PASSO 3: Descobrir quantos centavos sobraram.
        # O operador % devolve o resto da divisão.
        # Exemplo: 10000 % 3 = 1.
        centavos_restantes = (
            valor_em_centavos % self.quantidade_parcelas
        )

        # PASSO 4: Criar uma lista vazia para guardar os valores calculados.
        parcelas = []

        # PASSO 5: Gerar cada parcela.
        for numero in range(self.quantidade_parcelas):

            # Todas começam com o valor básico.
            valor_parcela = valor_base

            # Distribui um centavo adicional nas primeiras parcelas, enquanto houver sobra.
            if numero < centavos_restantes:
                valor_parcela += 1

            # Converte o valor novamente para reais.
            valor_em_reais = (
                Decimal(valor_parcela) / Decimal("100")
            )

            # Adiciona o valor calculado à lista.
            parcelas.append(valor_em_reais)

        # PASSO 6: Devolver a lista de parcelas.
        return parcelas