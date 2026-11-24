from decimal import Decimal

class AdaptadorCadastroCompra:
    """
    Adapta os dados recebidos pela API
    para a interface do ServicoCompras.
    """
    def __init__(self, servico_compras):
        self.servico_compras = servico_compras
    def cadastrar(self, dados):
        return self.servico_compras.cadastrar_compra(
            nome_cartao=dados.nome_cartao,
            descricao=dados.descricao,
            valor_total=Decimal(dados.valor_total),
            data_compra=dados.data_compra,
            quantidade_parcelas=dados.quantidade_parcelas,
            identificacao_fatura=dados.identificacao_fatura
        )