# Domínio: as regras do negócio

O "coração" do sistema. Aqui ficam as regras puras: como dividir uma compra em parcelas, em qual fatura cada parcela cai, como dividir um gasto entre pessoas.

**Regra da pasta:** nada aqui pode depender de banco de dados, API ou planilha. Se precisar guardar ou buscar dados, isso é feito por uma porta (veja `src/aplicacao`).
