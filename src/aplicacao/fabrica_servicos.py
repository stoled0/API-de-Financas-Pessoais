"""
Factory Method - Criacao dos componentes da API.

A fabrica organiza a criacao dos repositorios e a montagem dos servicos.
"""

from abc import ABC, abstractmethod

from src.aplicacao.servico_cartoes import ServicoCartoes
from src.aplicacao.servico_compras import ServicoCompras
from src.aplicacao.servico_despesas import ServicoDespesas
from src.aplicacao.servico_resumo import ServicoResumo

from src.persistencia.repositorio_cartoes import RepositorioCartoes
from src.persistencia.repositorio_compras import RepositorioCompras
from src.persistencia.repositorio_despesas import RepositorioDespesas
from src.persistencia.repositorio_resumo import RepositorioResumo


class FabricaServicos(ABC):
    """Define como os servicos serao montados."""

    @abstractmethod
    def criar_repositorios(self):
        """Cada fabrica escolhe os repositorios."""
        pass

    def criar_servicos(self):
        # Pede a fabrica os repositorios.
        repositorios = self.criar_repositorios()

        # Entrega os repositorios aos servicos.
        servico_cartoes = ServicoCartoes(
            repositorios["cartoes"]
        )
        servico_compras = ServicoCompras(
            repositorios["compras"],
            repositorios["cartoes"]
        )
        servico_despesas = ServicoDespesas(
            repositorios["despesas"]
        )
        servico_resumo = ServicoResumo(
            repositorios["resumo"],
            servico_despesas
        )
        # Devolve todos os servicos preparados.
        return {
            "cartoes": servico_cartoes,
            "compras": servico_compras,
            "despesas": servico_despesas,
            "resumo": servico_resumo
        }

class FabricaSQLite(FabricaServicos):
    """Cria os repositorios reais do SQLite."""
    def criar_repositorios(self):
        return {
            "cartoes": RepositorioCartoes(),
            "compras": RepositorioCompras(),
            "despesas": RepositorioDespesas(),
            "resumo": RepositorioResumo()
        }