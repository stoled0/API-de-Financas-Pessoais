from datetime import date
from decimal import Decimal
from src.dominio.despesa_recorrente import DespesaRecorrente
from src.persistencia.repositorio_despesas import RepositorioDespesas

class ServicoDespesas:
    def __init__(self, repositorio=None):
        self.repositorio = (
            repositorio
            if repositorio is not None
            else RepositorioDespesas()
        )

    # Coordena o cadastro da despesa.
    def cadastrar_despesa(
        self,
        descricao: str,
        valor_mensal: Decimal,
        dia_vencimento: int,
        data_inicio: date,
        data_fim: date | None = None
    ):

        # O domínio valida os dados.
        despesa = DespesaRecorrente(
            descricao=descricao,
            valor_mensal=valor_mensal,
            dia_vencimento=dia_vencimento,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        # O Repository salva a despesa.
        identificador = self.repositorio.salvar(despesa)

        return {
            "id": identificador,
            "descricao": despesa.descricao,
            "valor_mensal": str(despesa.valor_mensal),
            "dia_vencimento": despesa.dia_vencimento,
            "data_inicio": despesa.data_inicio.isoformat(),
            "data_fim": (
                despesa.data_fim.isoformat()
                if despesa.data_fim is not None
                else None
            )
        }

    # Consulta as despesas cadastradas.
    def listar_despesas(self):
        return self.repositorio.listar()

    # Calcula as cobranças de um mês específico.
    def consultar_cobrancas(self, ano: int, mes: int):
        if not 1 <= ano <= 9999:
            raise ValueError("O ano informado é inválido.")
        if not 1 <= mes <= 12:
            raise ValueError("O mês deve estar entre 1 e 12.")

        despesas = self.repositorio.listar()
        cobrancas = []

        for registro in despesas:
            # Reconstrói o objeto de domínio.
            despesa = DespesaRecorrente(
                descricao=registro["descricao"],
                valor_mensal=Decimal(
                    registro["valor_mensal"]
                ),
                dia_vencimento=registro["dia_vencimento"],
                data_inicio=date.fromisoformat(
                    registro["data_inicio"]
                ),
                data_fim=(
                    date.fromisoformat(registro["data_fim"])
                    if registro["data_fim"] is not None
                    else None
                )
            )

            # Solicita ao domínio a geração da cobrança.
            resultado = despesa.gerar_cobrancas(
                ano, mes, ano, mes
            )

            for cobranca in resultado:
                cobrancas.append({
                    "id_despesa": registro["id"],
                    "descricao": cobranca["descricao"],
                    "valor": str(cobranca["valor"]),
                    "ano": cobranca["ano"],
                    "mes": cobranca["mes"],
                    "dia_vencimento": cobranca["dia_vencimento"]
                })

        # Ordena as cobranças pelo dia.
        cobrancas.sort(
            key=lambda item: (
                item["dia_vencimento"],
                item["id_despesa"]
            )
        )

        return cobrancas