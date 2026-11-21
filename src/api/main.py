from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.aplicacao.servico_cartoes import ServicoCartoes
from src.persistencia.BD import criar_tabelas
from datetime import date
from decimal import Decimal, InvalidOperation
from src.aplicacao.servico_compras import ServicoCompras

# Cria as tabelas necessárias.
criar_tabelas()

# Configura a API.
app = FastAPI(
    title="API de Finanças Pessoais",
    description=(
        "Sistema de controle de cartões, "
        "compras parceladas e despesas fixas."
    ),
    version="1.0.0"
)
servico_cartoes = ServicoCartoes()
servico_compras = ServicoCompras()

# Dados obrigatórios para cadastrar um cartão.
class DadosCadastroCartao(BaseModel):
    nome: str = Field(..., examples=["Nubank"])
    dia_fechamento: int = Field(..., examples=[3])
    dia_vencimento: int = Field(..., examples=[10])

# Dados opcionais para editar um cartão.
class DadosEdicaoCartao(BaseModel):
    nome: str | None = None
    dia_fechamento: int | None = None
    dia_vencimento: int | None = None


# Define os dados recebidos no cadastro de compras.
class DadosCadastroCompra(BaseModel):
    # O usuário informa o nome, não o ID do cartão.
    nome_cartao: str = Field(
        ...,
        description="Nome de um cartão já cadastrado.",
        examples=["Nubank"]
    )

    descricao: str = Field(
        ...,
        description="Descrição da compra.",
        examples=["Notebook"]
    )

    # Recebemos como texto para preservar os centavos.
    valor_total: str = Field(
        ...,
        description="Valor em reais, com ponto decimal.",
        examples=["3000.00"]
    )

    # Se não informar a data, usamos a data atual.
    data_compra: date = Field(
        default_factory=date.today,
        description="Data em que a compra foi realizada."
    )

    quantidade_parcelas: int = Field(
        ...,
        description="Quantidade de parcelas, de 1 a 48.",
        examples=[3]
    )

    identificacao_fatura: str = Field(
        default="",
        description="Nome que aparece na fatura (opcional).",
        examples=["LOJA XYZ"]
    )

# Converte erros conhecidos em respostas HTTP.
def tratar_erro(erro):
    if isinstance(erro, LookupError):
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        ) from erro
    if isinstance(erro, ValueError):
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        ) from erro
    raise erro

@app.get("/", tags=["Sistema"])
def pagina_inicial():
    return {
        "mensagem": "API de Finanças Pessoais funcionando!"
    }

@app.post(
    "/cartoes",
    status_code=201,
    tags=["Cartões de crédito"],
    summary="Cadastrar cartão"
)
def cadastrar_cartao(dados: DadosCadastroCartao):
    try:
        return servico_cartoes.cadastrar_cartao(
            dados.nome,
            dados.dia_fechamento,
            dados.dia_vencimento
        )
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

@app.get(
    "/cartoes",
    tags=["Cartões de crédito"],
    summary="Listar cartões"
)
def listar_cartoes():
    return servico_cartoes.listar_cartoes()

@app.get(
    "/cartoes/{nome}",
    tags=["Cartões de crédito"],
    summary="Consultar cartão pelo nome"
)
def consultar_cartao(nome: str):
    try:
        return servico_cartoes.consultar_cartao(nome)
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

@app.patch(
    "/cartoes/{nome}",
    tags=["Cartões de crédito"],
    summary="Editar cartão pelo nome"
)
def editar_cartao(nome: str, dados: DadosEdicaoCartao):
    try:
        return servico_cartoes.editar_cartao(
            nome_atual=nome,
            novo_nome=dados.nome,
            dia_fechamento=dados.dia_fechamento,
            dia_vencimento=dados.dia_vencimento
        )
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

@app.delete(
    "/cartoes/{nome}",
    tags=["Cartões de crédito"],
    summary="Excluir cartão pelo nome"
)
def excluir_cartao(nome: str):
    try:
        return servico_cartoes.excluir_cartao(nome)
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# CADASTRAR COMPRA
@app.post(
    "/compras",
    status_code=201,
    tags=["Compras parceladas"],
    summary="Cadastrar compra no cartão"
)
def cadastrar_compra(dados: DadosCadastroCompra):
    try:
        # Converte o valor recebido para Decimal.
        valor = Decimal(dados.valor_total)

        # Solicita ao serviço o cadastro completo.
        return servico_compras.cadastrar_compra(
            nome_cartao=dados.nome_cartao,
            descricao=dados.descricao,
            valor_total=valor,
            data_compra=dados.data_compra,
            quantidade_parcelas=dados.quantidade_parcelas,
            identificacao_fatura=dados.identificacao_fatura
        )
    except InvalidOperation as erro:
        raise HTTPException(
            status_code=400,
            detail="O valor total deve ser um número válido."
        ) from erro
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# LISTAR COMPRAS
@app.get(
    "/compras",
    tags=["Compras parceladas"],
    summary="Consultar compras e parcelas"
)
def listar_compras():
    return servico_compras.listar_compras()