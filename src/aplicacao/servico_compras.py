from datetime import date
from decimal import Decimal

from src.dominio.compra import Compra
from src.dominio.gerador_parcelas import gerar_parcelas

from src.dominio.contratos_repositorios import ConsultaCartoes, RegistroCompras

class ServicoCompras:
    def __init__(
        self,
        repositorio_compras: RegistroCompras,
        repositorio_cartoes: ConsultaCartoes
    ):
        self.repositorio_compras = repositorio_compras
        self.repositorio_cartoes = repositorio_cartoes

    # Coordena o cadastro completo de uma compra.
    def cadastrar_compra(
        self,
        nome_cartao: str,
        descricao: str,
        valor_total: Decimal,
        data_compra: date,
        quantidade_parcelas: int,
        identificacao_fatura: str = ""
    ):

        # ETAPA 1: Localizar o cartão pelo nome.
        cartao = self.repositorio_cartoes.buscar_por_nome(
            nome_cartao
        )
        if cartao is None:
            raise ValueError(
                "O cartão informado não está cadastrado."
            )

        # ETAPA 2: Criar a compra.
        # A classe Compra valida os dados automaticamente.
        compra = Compra(
            cartao_id=cartao["id"],
            descricao=descricao,
            valor_total=valor_total,
            data_compra=data_compra,
            quantidade_parcelas=quantidade_parcelas,
            identificacao_fatura=identificacao_fatura
        )

        # ETAPA 3: Calcular valores e vencimentos.
        parcelas = gerar_parcelas(
            compra=compra,
            dia_fechamento=cartao["dia_fechamento"],
            dia_vencimento=cartao["dia_vencimento"]
        )

        # ETAPA 4: Salvar compra e parcelas no banco.
        compra_id = self.repositorio_compras.salvar(
            compra,
            parcelas
        )

        # ETAPA 5: Devolver o resultado do cadastro.
        return {
            "id": compra_id,
            "nome_cartao": cartao["nome"],
            "descricao": compra.descricao,
            "identificacao_fatura": compra.identificacao_fatura,
            "valor_total": str(compra.valor_total),
            "data_compra": compra.data_compra.isoformat(),
            "quantidade_parcelas": compra.quantidade_parcelas,
            "parcelas": [
                {
                    "numero": parcela["numero"],
                    "total_parcelas": parcela["total_parcelas"],
                    "valor": str(parcela["valor"]),
                    "vencimento": parcela["vencimento"].isoformat()
                }
                for parcela in parcelas
            ]
        }

    # Consulta as compras registradas.
    def listar_compras(self):
        return self.repositorio_compras.listar()