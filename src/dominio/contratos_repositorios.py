"""Contratos utilizados pelos serviços da API.

Esse arquivo não executa consultas e não salva informações. Ele apenas define o que cada componente precisa saber fazer.
Os contratos definem quais operações cada serviço precisa utilizar, sem depender diretamente do SQLite.

Princípios aplicados:
DIP - Inversão de Dependência
ISP - Segregação de Interfaces
"""

from typing import Protocol


# Contrato para consultar cartões.
# Utilizado pelo serviço de compras.
class ConsultaCartoes(Protocol):
    def buscar_por_nome(self, nome: str): ...


# Contrato para gerenciar cartões.
# Utilizado pelo serviço de cartões.
class GestaoCartoes(ConsultaCartoes, Protocol):
    def salvar(self, cartao): ...
    def listar(self): ...
    def buscar_por_id(self, cartao_id): ...
    def possui_compras(self, cartao_id): ...
    def atualizar(self, cartao_id, cartao): ...
    def excluir(self, cartao_id): ...


# Contrato para registrar e consultar compras.
class RegistroCompras(Protocol):
    def salvar(self, compra, parcelas): ...
    def listar(self): ...


# Contrato para registrar e consultar despesas.
class RegistroDespesas(Protocol):
    def salvar(self, despesa): ...
    def listar(self): ...


# Contrato para consultar os valores dos cartões.
class ConsultaResumoCartoes(Protocol):
    def consultar_cartoes(self, ano: int, mes: int): ...


# Contrato para consultar cobranças recorrentes.
class ConsultaCobrancas(Protocol):
    def consultar_cobrancas(self, ano: int, mes: int): ...
