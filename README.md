# API de Finanças Pessoais

Trabalho acadêmico desenvolvido na disciplina de Engenharia de Software do Instituto Federal de Minas Gerais (IFMG) — Campus Ribeirão das Neves.

## 1. Objetivo do projeto

Desenvolver uma API REST para auxiliar na organização de compras realizadas com cartões de crédito e despesas mensais recorrentes.

O sistema permitirá cadastrar cartões, registrar compras parceladas, organizar automaticamente as parcelas nas respectivas faturas e consultar resumos financeiros mensais. A proposta é automatizar cálculos e organizar informações financeiras, reduzindo a necessidade de realizar esses controles manualmente.

## 2. Funcionalidades previstas

O sistema será composto por cinco funcionalidades principais.

**PB-01 — Cadastro de cartões de crédito**

Permitir o cadastro e a consulta de cartões, contendo nome, dia de fechamento e dia de vencimento.

**PB-02 — Registro de compras**

Permitir o registro de compras realizadas no cartão de crédito, contendo descrição, valor total, data da compra, cartão utilizado e quantidade de parcelas de 1 a 48. A identificação apresentada na fatura será opcional.

**PB-03 — Parcelamento e organização de faturas**

Calcular automaticamente o valor das parcelas, distribuir corretamente os centavos e identificar a fatura correspondente a cada parcela, considerando o dia de fechamento do cartão.

**PB-04 — Despesas recorrentes**

Permitir o cadastro de despesas mensais de valor fixo, contendo descrição, valor, data de início, data de término opcional e dia de vencimento.

**PB-05 — Resumo financeiro mensal**

Permitir a consulta dos valores das faturas de cartão e das despesas recorrentes de determinado mês, apresentando o total financeiro sem duplicar registros.

## 3. Principais regras do sistema

- Cada cartão deverá possuir nome, dia de fechamento e dia de vencimento.
- As compras deverão estar associadas a um cartão previamente cadastrado.
- Compras realizadas no dia do fechamento serão incluídas na fatura atual.
- A soma das parcelas deverá corresponder exatamente ao valor total da compra.
- As despesas recorrentes serão geradas mensalmente, respeitando suas datas de início e término.
- Para despesas recorrentes, os dias de vencimento vão de 1 a 31 e são tratados como números, sem ajustes por calendário, dias úteis ou feriados.
- As despesas recorrentes geram uma cobrança por mês dentro do período de vigência, sem registrar cópias mensais no banco.
- Os casos especiais de fechamento e vencimento dos cartões nos dias 29, 30 e 31 não serão tratados na versão inicial.

## 4. Funcionalidades fora do escopo

Não serão desenvolvidas nesta versão funcionalidades relacionadas a Pix, débito, dinheiro, receitas, divisão de compras entre pessoas, importação de planilhas, controle de pagamentos, antecipação de parcelas ou interface gráfica própria.

Também não serão implementadas funcionalidades de edição ou cancelamento de compras já registradas.

## 5. Tecnologias utilizadas ou planejadas

- **Python:** linguagem utilizada no desenvolvimento das funcionalidades.
- **FastAPI:** framework escolhido para criação da API REST.
- **SQLite:** banco de dados relacional escolhido para armazenamento das informações.
- **Repository:** padrão de projeto utilizado para organizar o acesso aos dados.
- **pytest:** ferramenta utilizada para os testes automatizados.
- **Swagger UI:** interface interativa para documentação e demonstração da API.
- **Git e GitHub:** ferramentas de versionamento e colaboração.

## 6. Arquitetura do sistema

O projeto utilizará uma arquitetura em camadas, organizada em quatro responsabilidades principais.

```text
src/
    api/
    aplicacao/
    dominio/
    persistencia/

tests/
docs/
```

**API:** responsável por receber requisições HTTP e retornar respostas.

**Aplicação:** responsável por coordenar as operações solicitadas.

**Domínio:** responsável por representar os elementos financeiros e implementar as regras de negócio.

**Persistência:** responsável pelo armazenamento e recuperação dos dados no SQLite.

Essa organização busca facilitar a compreensão, a manutenção e os testes do sistema.

## 7. Situação atual do desenvolvimento

As cinco funcionalidades do escopo estão implementadas: cartões, compras, parcelamento, despesas recorrentes e resumo mensal. Os quatro blocos de testes automatizados foram executados em conjunto, com 80 testes aprovados na revisão.

## 8. Como executar a API e os testes

Na pasta principal do projeto, com Python e as dependências instaladas, inicie a API:

```powershell
python -m uvicorn src.api.main:app --reload
```

Acesse a interface Swagger em `http://127.0.0.1:8000/docs`.

Para executar os testes automatizados:

```powershell
python -m pytest tests/test_bloco1_cartoes.py tests/test_bloco2_compras.py tests/test_bloco3_despesas.py tests/test_bloco4_resumo.py -v
```

Para consultar a cobertura dos módulos de domínio:

```powershell
python -m pytest tests/test_bloco1_cartoes.py tests/test_bloco2_compras.py tests/test_bloco3_despesas.py tests/test_bloco4_resumo.py --cov=src.dominio --cov-report=term-missing
```

## 9. Organização do desenvolvimento

O projeto será desenvolvido de maneira incremental, dividido em três Sprints.

- **Sprint 1:** cadastro de cartões de crédito.
- **Sprint 2:** registro de compras, parcelamento e organização de faturas.
- **Sprint 3:** despesas recorrentes e resumo financeiro mensal.

As decisões arquiteturais e os requisitos estão documentados no Relatório Técnico do projeto.

Os arquivos da pasta `docs/` serão utilizados como documentação complementar de apoio ao desenvolvimento.