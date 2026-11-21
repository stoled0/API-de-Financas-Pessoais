# Importa a classe Cartao, responsável por validar os dados.
from src.dominio.cartao import Cartao

# Importa a classe responsável por salvar e consultar cartões.
from src.persistencia.repositorio_cartoes import RepositorioCartoes

# Importa a função que garante que a tabela exista.
from src.persistencia.BD import criar_tabelas

# ETAPA 1: PREPARAR O BANCO DE DADOS
# Garante que a tabela de cartões exista antes do teste.
criar_tabelas()

# ETAPA 2: CRIAR UM CARTÃO
# Cria um cartão utilizando a classe do domínio.
# A classe Cartao verifica se os dados são válidos.
cartao_nubank = Cartao(
    nome="Nubank",
    dia_fechamento=3,
    dia_vencimento=10,
)
print("Cartão criado e validado com sucesso!")

# ETAPA 3: CRIAR O REPOSITORY
# Cria um objeto responsável pelas operações no banco.
repositorio = RepositorioCartoes()

# ETAPA 4: SALVAR O CARTÃO
# Envia o objeto Cartao para o método salvar().
# O método executa o INSERT INTO no SQLite.
identificador = repositorio.salvar(cartao_nubank)

print("Cartão salvo no banco de dados!")
print("ID gerado:", identificador)


# ETAPA 5: CONSULTAR OS CARTÕES
# Executa o SELECT para recuperar os cartões cadastrados.
cartoes_cadastrados = repositorio.listar()

print("\nCartões encontrados no banco:")

# Percorre a lista e mostra os dados de cada cartão.
for cartao in cartoes_cadastrados:

    print("ID:", cartao["id"])
    print("Nome:", cartao["nome"])
    print("Fechamento:", cartao["dia_fechamento"])
    print("Vencimento:", cartao["dia_vencimento"])

    print("----------------------------")

# ETAPA 6: VERIFICAR O RESULTADO
# Procura o cartão utilizando o ID gerado no cadastro.
cartao_encontrado = False

for cartao in cartoes_cadastrados:
    if cartao["id"] == identificador:

        # Confere se os dados recuperados estão corretos.
        assert cartao["nome"] == "Nubank"
        assert cartao["dia_fechamento"] == 3
        assert cartao["dia_vencimento"] == 10

        cartao_encontrado = True

# Confirma que o cartão foi encontrado.
assert cartao_encontrado

print("\nTESTE CONCLUÍDO COM SUCESSO!")