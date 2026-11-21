from datetime import date
from src.dominio.calculo_faturas import (
    calcular_primeiro_vencimento,
    calcular_datas_parcelas
)

# TESTE 1: Compra antes do fechamento.
vencimento = calcular_primeiro_vencimento(
    data_compra=date(2026, 11, 2),
    dia_fechamento=3,
    dia_vencimento=10
)

assert vencimento == date(2026, 11, 10)
print("Teste 1: compra antes do fechamento - OK")

# TESTE 2: Compra no dia do fechamento.
vencimento = calcular_primeiro_vencimento(
    data_compra=date(2026, 11, 3),
    dia_fechamento=3,
    dia_vencimento=10
)
assert vencimento == date(2026, 11, 10)
print("Teste 2: compra no fechamento - OK")

# TESTE 3: Compra depois do fechamento.
vencimento = calcular_primeiro_vencimento(
    data_compra=date(2026, 11, 4),
    dia_fechamento=3,
    dia_vencimento=10
)

assert vencimento == date(2026, 12, 10)
print("Teste 3: compra depois do fechamento - OK")

# TESTE 4: Parcelamento atravessando o ano.
datas = calcular_datas_parcelas(
    data_compra=date(2026, 11, 4),
    dia_fechamento=3,
    dia_vencimento=10,
    quantidade_parcelas=3
)

assert datas == [
    date(2026, 12, 10),
    date(2027, 1, 10),
    date(2027, 2, 10)
]
print("Teste 4: parcelamento entre anos - OK")

# TESTE 5: Vencimento no mês seguinte ao fechamento.
vencimento = calcular_primeiro_vencimento(
    data_compra=date(2026, 11, 20),
    dia_fechamento=25,
    dia_vencimento=5
)

assert vencimento == date(2026, 12, 5)
print("Teste 5: vencimento no mês seguinte - OK")
print("\nTODOS OS TESTES DE FATURAS PASSARAM!")