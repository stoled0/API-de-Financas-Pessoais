from datetime import date
from decimal import Decimal

import pytest

from src.dominio.compra import Compra


def test_impedir_parcelas_com_valor_zero():
    with pytest.raises(
        ValueError, match=r"Cada parcela deve possuir valor mínimo de R\$ 0,01\."
    ):
        Compra(
            cartao_id=1,
            descricao="Compra teste TDD",
            valor_total=Decimal("0.02"),
            data_compra=date(2026, 11, 10),
            quantidade_parcelas=3,
        )
