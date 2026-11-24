from abc import ABC, abstractmethod
from src.dominio.calculo_faturas import calcular_datas_parcelas

class GeradorParcelas(ABC):
    """
    Define a sequencia de etapas para gerar parcelas.
    """

    # TEMPLATE METHOD: define a ordem das etapas.
    def gerar(self, compra, dia_fechamento, dia_vencimento):
        # ETAPA 1: Calcular os valores.
        valores = self.calcular_valores(compra)

        # ETAPA 2: Calcular os vencimentos.
        datas = self.calcular_vencimentos(
            compra,
            dia_fechamento,
            dia_vencimento
        )

        # ETAPA 3: Reunir valores e vencimentos.
        parcelas = []

        for indice in range(compra.quantidade_parcelas):
            parcela = {
                "numero": indice + 1,
                "total_parcelas": compra.quantidade_parcelas,
                "valor": valores[indice],
                "vencimento": datas[indice]
            }

            parcelas.append(parcela)

        # ETAPA 4: Devolver as parcelas.
        return parcelas

    @abstractmethod
    def calcular_valores(self, compra):
        pass
    @abstractmethod
    def calcular_vencimentos(
        self, compra, dia_fechamento, dia_vencimento
    ):
        pass


class GeradorParcelasCartao(GeradorParcelas):
    """
    Implementa as etapas especificas do cartao de credito.
    """
    def calcular_valores(self, compra):
        return compra.calcular_parcelas()

    def calcular_vencimentos(
        self, compra, dia_fechamento, dia_vencimento
    ):
        return calcular_datas_parcelas(
            data_compra=compra.data_compra,
            dia_fechamento=dia_fechamento,
            dia_vencimento=dia_vencimento,
            quantidade_parcelas=compra.quantidade_parcelas
        )


# Mantem a interface utilizada pelo restante do sistema.
def gerar_parcelas(
    compra,
    dia_fechamento,
    dia_vencimento
):
    gerador = GeradorParcelasCartao()

    return gerador.gerar(
        compra,
        dia_fechamento,
        dia_vencimento
    )
