from src.dominio.cartao import Cartao

# TESTE 1: Cartão válido
print("TESTE 1 - CARTÃO VÁLIDO")

cartao_nubank = Cartao(
    nome="Nubank",
    dia_fechamento=5,
    dia_vencimento=12
)
print("Cartão criado:", cartao_nubank.nome)


# TESTE 2: Cartão com dia de fechamento inválido
print()
print("TESTE 2 - FECHAMENTO INVÁLIDO")

try:
    cartao_inter = Cartao(
        nome="Inter",
        dia_fechamento=0,
        dia_vencimento=15
    )
except ValueError as erro:
    print("Erro identificado:", erro)


# TESTE 3: Cartão sem nome
print()
print("TESTE 3 - NOME VAZIO")

try:
    cartao_picpay = Cartao(
        nome="",
        dia_fechamento=8,
        dia_vencimento=15
    )
except ValueError as erro:
    print("Erro identificado:", erro)
