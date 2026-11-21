"""
API DE FINANÇAS PESSOAIS

Este arquivo é a porta de entrada da nossa API.

Ele recebe as requisições HTTP, encaminha as informações
para os serviços e devolve as respostas ao usuário.

Bloco 1: Cartões
Bloco 2: Compras parceladas
Bloco 3: Despesas fixas e recorrentes
"""

from datetime import date
from decimal import Decimal, InvalidOperation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.persistencia.BD import criar_tabelas
from src.aplicacao.servico_cartoes import ServicoCartoes
from src.aplicacao.servico_compras import ServicoCompras
from src.aplicacao.servico_despesas import ServicoDespesas
from src.aplicacao.servico_resumo import ServicoResumo

# ============================================================
# 1. CONFIGURAÇÃO DA API
# ============================================================

app = FastAPI(
    title="API de Finanças Pessoais",
    description=(
        "API para gerenciamento de cartões de crédito, "
        "compras parceladas e despesas recorrentes."
    ),
    version="1.0.0"
)

# Cria as tabelas do banco, caso ainda não existam.
criar_tabelas()

# ============================================================
# 2. INICIALIZAÇÃO DOS SERVIÇOS
# ============================================================

# Os serviços coordenam as regras de negócio.
servico_cartoes = ServicoCartoes()
servico_compras = ServicoCompras()
servico_despesas = ServicoDespesas()
servico_resumo = ServicoResumo(
    servico_despesas=servico_despesas
)

# ============================================================
# 3. MODELOS PYDANTIC
# ============================================================

# Os modelos definem os dados recebidos pelo Swagger.

# ---------------------------
# 3.1. Cadastro de cartão
# ---------------------------
class DadosCadastroCartao(BaseModel):
    nome: str = Field(
        ...,
        examples=["Nubank"]
    )
    dia_fechamento: int = Field(
        ...,
        examples=[25]
    )
    dia_vencimento: int = Field(
        ...,
        examples=[5]
    )

# ---------------------------
# 3.2. Edição de cartão
# ---------------------------
class DadosEdicaoCartao(BaseModel):
    nome: str | None = None
    dia_fechamento: int | None = None
    dia_vencimento: int | None = None

# ---------------------------
# 3.3. Cadastro de compra
# ---------------------------
class DadosCadastroCompra(BaseModel):
    nome_cartao: str = Field(
        ...,
        examples=["Nubank"]
    )
    descricao: str = Field(
        ...,
        examples=["Notebook"]
    )
    valor_total: str = Field(
        ...,
        examples=["3000.00"]
    )
    data_compra: date = Field(
        default_factory=date.today
    )
    quantidade_parcelas: int = Field(
        ...,
        examples=[3]
    )
    identificacao_fatura: str = Field(
        default=""
    )

# ---------------------------
# 3.4. Cadastro de despesa
# ---------------------------
class DadosCadastroDespesa(BaseModel):
    descricao: str = Field(
        ...,
        examples=["Internet residencial"]
    )
    valor_mensal: str = Field(
        ...,
        examples=["120.00"]
    )
    dia_vencimento: int = Field(
        ...,
        examples=[10]
    )
    data_inicio: date = Field(
        ...,
        examples=["2026-11-01"]
    )
    data_fim: date | None = Field(
        default=None,
        description="Opcional. Deixe null se não houver término."
    )

# ============================================================
# 4. TRATAMENTO DE ERROS
# ============================================================
def tratar_erro(erro):
    # Quando o registro não é encontrado.
    if isinstance(erro, LookupError):
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        ) from erro
    # Quando uma regra de negócio não é atendida.
    raise HTTPException(
        status_code=400,
        detail=str(erro)
    ) from erro

# ============================================================
# 5. ROTAS DOS CARTÕES — BLOCO 1
# ============================================================

# CADASTRAR CARTÃO
@app.post(
    "/cartoes",
    status_code=201,
    tags=["Cartões"]
)
def cadastrar_cartao(dados: DadosCadastroCartao):
    try:
        return servico_cartoes.cadastrar_cartao(
            nome=dados.nome,
            dia_fechamento=dados.dia_fechamento,
            dia_vencimento=dados.dia_vencimento
        )
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# LISTAR CARTÕES
@app.get(
    "/cartoes",
    tags=["Cartões"]
)
def listar_cartoes():
    return servico_cartoes.listar_cartoes()

# CONSULTAR CARTÃO PELO NOME
@app.get(
    "/cartoes/{nome}",
    tags=["Cartões"]
)
def consultar_cartao(nome: str):
    try:
        return servico_cartoes.consultar_cartao(nome)

    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# EDITAR CARTÃO
@app.patch(
    "/cartoes/{nome}",
    tags=["Cartões"]
)
def editar_cartao(
    nome: str,
    dados: DadosEdicaoCartao
):

    try:
        return servico_cartoes.editar_cartao(
            nome,
            novo_nome=dados.nome,
            dia_fechamento=dados.dia_fechamento,
            dia_vencimento=dados.dia_vencimento
        )

    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# EXCLUIR CARTÃO
@app.delete(
    "/cartoes/{nome}",
    tags=["Cartões"]
)
def excluir_cartao(nome: str):
    try:
        return servico_cartoes.excluir_cartao(nome)

    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# ============================================================
# 6. ROTAS DAS COMPRAS — BLOCO 2
# ============================================================

# CADASTRAR COMPRA PARCELADA
@app.post(
    "/compras",
    status_code=201,
    tags=["Compras parceladas"]
)
def cadastrar_compra(dados: DadosCadastroCompra):
    try:
        # Converte o valor recebido para Decimal.
        valor = Decimal(dados.valor_total)

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
    tags=["Compras parceladas"]
)
def listar_compras():
    return servico_compras.listar_compras()

# ============================================================
# 7. ROTAS DAS DESPESAS RECORRENTES — BLOCO 3
# ============================================================

# CADASTRAR DESPESA
@app.post(
    "/despesas",
    status_code=201,
    tags=["Despesas recorrentes"]
)
def cadastrar_despesa(dados: DadosCadastroDespesa):
    try:
        valor = Decimal(dados.valor_mensal)

        return servico_despesas.cadastrar_despesa(
            descricao=dados.descricao,
            valor_mensal=valor,
            dia_vencimento=dados.dia_vencimento,
            data_inicio=dados.data_inicio,
            data_fim=dados.data_fim
        )

    except InvalidOperation as erro:
        raise HTTPException(
            status_code=400,
            detail="O valor mensal deve ser um número válido."
        ) from erro

    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# LISTAR DESPESAS
@app.get(
    "/despesas",
    tags=["Despesas recorrentes"]
)
def listar_despesas():
    return servico_despesas.listar_despesas()

# CONSULTAR COBRANÇAS DE UM MÊS
@app.get(
    "/despesas/cobrancas/{ano}/{mes}",
    tags=["Despesas recorrentes"]
)
def consultar_cobrancas(ano: int, mes: int):
    try:
        return servico_despesas.consultar_cobrancas(
            ano,
            mes
        )
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)

# ============================================================
# 8. RESUMO FINANCEIRO MENSAL — BLOCO 4
# ============================================================

@app.get(
    "/resumo/{ano}/{mes}",
    tags=["Resumo financeiro"],
    summary="Consultar resumo financeiro mensal"
)
def consultar_resumo(ano: int, mes: int):
    try:
        return servico_resumo.consultar_resumo(
            ano,
            mes
        )
    except (ValueError, LookupError) as erro:
        tratar_erro(erro)