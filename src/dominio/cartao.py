class Cartao:
    def __init__(
        self,
        nome: str,
        dia_fechamento: int,
        dia_vencimento: int
    ):

        # Verificar se o nome foi informado
        if not isinstance(nome, str):
            raise ValueError("O nome do cartão deve ser um texto.")

        if nome.strip() == "":
            raise ValueError("O nome do cartão é obrigatório.")

        # Verificar o dia de fechamento
        if type(dia_fechamento) is not int:
            raise ValueError("O dia de fechamento deve ser um número inteiro.")

        if dia_fechamento < 1 or dia_fechamento > 28:
            raise ValueError(
                "O dia de fechamento deve estar entre 1 e 28."
            )

        # Verificar o dia de vencimento
        if type(dia_vencimento) is not int:
            raise ValueError("O dia de vencimento deve ser um número inteiro.")

        if dia_vencimento < 1 or dia_vencimento > 28:
            raise ValueError(
                "O dia de vencimento deve estar entre 1 e 28."
            )

        # Guardar os dados do cartão
        self.nome = nome.strip()
        self.dia_fechamento = dia_fechamento
        self.dia_vencimento = dia_vencimento
