from datetime import date
from decimal import Decimal
from src.dominio.compra import Compra

# Cria uma compra de exemplo.
compra = Compra(
    cartao_id=1,
    descricao="Compra de teste",
    valor_total=Decimal("100.00"),
    data_compra=date(2026, 11, 20),
    quantidade_parcelas=3
)

# Solicita o cálculo das parcelas.
parcelas = compra.calcular_parcelas()

# Mostra os valores calculados.
print("Parcelas calculadas:")

for numero, valor in enumerate(parcelas, start=1):
    print(f"Parcela {numero}: R$ {valor:.2f}")

# Verifica se a soma corresponde ao valor da compra.
assert sum(parcelas) == Decimal("100.00")

# Verifica se foram geradas exatamente três parcelas.
assert len(parcelas) == 3

# Confere os valores esperados.
assert parcelas == [
    Decimal("33.34"),
    Decimal("33.33"),
    Decimal("33.33")
]

print("\nTESTE DE PARCELAMENTO CONCLUÍDO COM SUCESSO!")