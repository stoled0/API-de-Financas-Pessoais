from src.dominio.cartao import Cartao
from src.dominio.contratos_repositorios import GestaoCartoes

class ServicoCartoes:
    def __init__(self, repositorio: GestaoCartoes):
        self.repositorio = repositorio

    # Cadastra um cartão novo.
    def cadastrar_cartao(
        self, nome, dia_fechamento, dia_vencimento
    ):
        cartao = Cartao(
            nome, dia_fechamento, dia_vencimento
        )
        identificador = self.repositorio.salvar(cartao)
        return {
            "id": identificador,
            "nome": cartao.nome,
            "dia_fechamento": cartao.dia_fechamento,
            "dia_vencimento": cartao.dia_vencimento
        }

    # Lista os cartões cadastrados.
    def listar_cartoes(self):
        return self.repositorio.listar()

    # Consulta um cartão pelo nome.
    def consultar_cartao(self, nome):
        cartao = self.repositorio.buscar_por_nome(nome)
        if cartao is None:
            raise LookupError("Cartão não encontrado.")
        return cartao

    # Edita um cartão identificado pelo nome atual.
    def editar_cartao(
        self,
        nome_atual,
        novo_nome=None,
        dia_fechamento=None,
        dia_vencimento=None
    ):
        atual = self.consultar_cartao(nome_atual)

        # Campos não informados mantêm seus valores.
        nome = (
            atual["nome"]
            if novo_nome is None
            else novo_nome
        )
        fechamento = (
            atual["dia_fechamento"]
            if dia_fechamento is None
            else dia_fechamento
        )
        vencimento = (
            atual["dia_vencimento"]
            if dia_vencimento is None
            else dia_vencimento
        )

        # Reutiliza as validações do domínio.
        cartao = Cartao(nome, fechamento, vencimento)

        # Protege os vencimentos de compras existentes.
        if self.repositorio.possui_compras(atual["id"]):
            if (
                fechamento != atual["dia_fechamento"]
                or vencimento != atual["dia_vencimento"]
            ):
                raise ValueError(
                    "Este cartão possui compras. "
                    "Somente o nome pode ser alterado."
                )
        atualizado = self.repositorio.atualizar(
            atual["id"], cartao
        )
        if not atualizado:
            raise ValueError(
                "Não foi possível atualizar o cartão. "
                "Verifique se existem compras vinculadas."
            )
        return self.repositorio.buscar_por_id(atual["id"])

    # Exclui um cartão identificado pelo nome.
    def excluir_cartao(self, nome):
        cartao = self.consultar_cartao(nome)
        if self.repositorio.possui_compras(cartao["id"]):
            raise ValueError(
                "Não é possível excluir um cartão "
                "que possui compras cadastradas."
            )
        excluido = self.repositorio.excluir(cartao["id"])

        if not excluido:
            raise ValueError(
                "Não foi possível excluir o cartão. "
                "Verifique se existem compras vinculadas."
            )
        return {
            "mensagem": "Cartão excluído com sucesso.",
            "nome": cartao["nome"]
        }