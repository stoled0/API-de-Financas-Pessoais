from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.aplicacao.servico_cartoes import ServicoCartoes
from src.persistencia.BD import criar_tabelas

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