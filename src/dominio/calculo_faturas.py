from datetime import date

# Avança uma quantidade de meses a partir de um ano e mês informados.
def adicionar_meses(ano, mes, quantidade):
    # Transforma ano e mês em uma contagem de meses.
    total_meses = ano * 12 + (mes - 1) + quantidade

    # Calcula o novo ano e o novo mês.
    novo_ano = total_meses // 12
    novo_mes = total_meses % 12 + 1
    return novo_ano, novo_mes

# Calcula a data de vencimento da primeira parcela.
def calcular_primeiro_vencimento(
    data_compra,
    dia_fechamento,
    dia_vencimento
):

    # Verifica se a data foi informada corretamente.
    if not isinstance(data_compra, date):
        raise ValueError("A data da compra é inválida.")

    # Por enquanto, utilizamos dias de 1 a 28 para fechamento e vencimento dos cartões.
    for dia in (dia_fechamento, dia_vencimento):
        if type(dia) is not int or not 1 <= dia <= 28:
            raise ValueError(
                "Os dias de fechamento e vencimento "
                "devem estar entre 1 e 28."
            )

    # Começamos considerando o mês da compra.
    ano_fatura = data_compra.year
    mes_fatura = data_compra.month

    # Se a compra aconteceu depois do fechamento, ela pertence ao próximo ciclo de fatura.
    if data_compra.day > dia_fechamento:
        ano_fatura, mes_fatura = adicionar_meses(
            ano_fatura, mes_fatura, 1
        )

    # Se o vencimento acontece no mesmo dia ou antes do fechamento, ele pertence ao mês seguinte ao fechamento.
    if dia_vencimento <= dia_fechamento:
        ano_fatura, mes_fatura = adicionar_meses(
            ano_fatura, mes_fatura, 1
        )

    # Devolve a data de vencimento calculada.
    return date(
        ano_fatura,
        mes_fatura,
        dia_vencimento
    )

# Gera as datas de vencimento de todas as parcelas.
def calcular_datas_parcelas(
    data_compra,
    dia_fechamento,
    dia_vencimento,
    quantidade_parcelas
):

    # Confere se a quantidade de parcelas é válida.
    if (
        type(quantidade_parcelas) is not int
        or not 1 <= quantidade_parcelas <= 48
    ):
        raise ValueError(
            "A quantidade de parcelas deve estar entre 1 e 48."
        )

    # Descobre quando vence a primeira parcela.
    primeiro_vencimento = calcular_primeiro_vencimento(
        data_compra,
        dia_fechamento,
        dia_vencimento
    )

    # Cria uma lista para guardar as datas.
    datas = []

    # Gera uma data de vencimento para cada parcela.
    for numero in range(quantidade_parcelas):

        # Avança um mês para cada nova parcela.
        ano, mes = adicionar_meses(
            primeiro_vencimento.year,
            primeiro_vencimento.month,
            numero
        )

        # Os vencimentos dos cartões vão de 1 a 28, então esse dia existe em todos os meses.
        datas.append(date(ano, mes, primeiro_vencimento.day))

    return datas