# Importa a função que calcula as datas das parcelas.
from src.dominio.calculo_faturas import calcular_datas_parcelas

# Esta função reúne os valores e as datas das parcelas. Ela recebe:
# - uma compra já validada;
# - o dia de fechamento do cartão;
# - o dia de vencimento do cartão.
def gerar_parcelas(
    compra,
    dia_fechamento,
    dia_vencimento
):

    # PASSO 1: Calcular os valores das parcelas.
    # Essa operação já existe no arquivo compra.py.
    valores = compra.calcular_parcelas()

    # PASSO 2: Calcular as datas de vencimento.
    # Essa operação já existe em calculo_faturas.py.
    datas = calcular_datas_parcelas(
        data_compra=compra.data_compra,
        dia_fechamento=dia_fechamento,
        dia_vencimento=dia_vencimento,
        quantidade_parcelas=compra.quantidade_parcelas
    )

    # PASSO 3: Preparar uma lista vazia.
    parcelas = []

    # PASSO 4: Reunir o valor e a data de cada parcela.
    for indice in range(compra.quantidade_parcelas):

        # O número da parcela começa em 1.
        numero_parcela = indice + 1

        # Reúne as informações da parcela.
        parcela = {
            "numero": numero_parcela,
            "total_parcelas": compra.quantidade_parcelas,
            "valor": valores[indice],
            "vencimento": datas[indice]
        }

        # Adiciona a parcela à lista.
        parcelas.append(parcela)

    # PASSO 5: Devolver todas as parcelas geradas.
    return parcelas