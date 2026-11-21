# Importa o Repository que estamos testando.
from src.persistencia.repositorio_cartoes import RepositorioCartoes

# Cria o objeto responsável por consultar os cartões.
repositorio = RepositorioCartoes()

# TESTE 1: Buscar o Nubank pelo nome correto.
cartao = repositorio.buscar_por_nome("Nubank")

assert cartao is not None
assert cartao["nome"] == "Nubank"
print("Teste 1: Nubank encontrado com sucesso!")

# TESTE 2: Buscar com letras maiúsculas e espaços.
cartao = repositorio.buscar_por_nome(" NUBANK ")
assert cartao is not None
assert cartao["id"] == 1
print("Teste 2: Busca ignorando maiúsculas e espaços funcionou!")

# TESTE 3: Buscar um cartão inexistente.
cartao = repositorio.buscar_por_nome("Cartão Inexistente")
assert cartao is None
print("Teste 3: Cartão inexistente identificado corretamente!")
print("\nTodos os testes de busca passaram!")