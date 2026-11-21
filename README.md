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
- Caso o dia de vencimento de uma despesa recorrente não exista no mês, a ocorrência será transferida para o primeiro dia útil do mês seguinte.
- Para as despesas recorrentes, serão considerados dias úteis de segunda a sexta-feira, sem tratamento de feriados.
- Para simplificação acadêmica, fevereiro será considerado com 28 dias.
- Os casos especiais de fechamento e vencimento dos cartões nos dias 29, 30 e 31 não serão tratados na versão inicial.

## 4. Funcionalidades fora do escopo

Não serão desenvolvidas nesta versão funcionalidades relacionadas a Pix, débito, dinheiro, receitas, divisão de compras entre pessoas, importação de planilhas, controle de pagamentos, antecipação de parcelas ou interface gráfica própria.

Também não serão implementadas funcionalidades de edição ou cancelamento de compras já registradas.

## 5. Tecnologias utilizadas ou planejadas

- **Python:** linguagem utilizada no desenvolvimento das funcionalidades.
- **FastAPI:** framework escolhido para criação da API REST.
- **SQLite:** banco de dados relacional escolhido para armazenamento das informações.
- **Repository:** padrão de projeto utilizado para organizar o acesso aos dados.
- **pytest:** ferramenta prevista para os testes automatizados.
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

O projeto encontra-se em desenvolvimento.

Até o momento, foram realizadas a definição do escopo, a organização inicial da arquitetura e a implementação da classe `Cartao`, com validações para nome obrigatório e dias de fechamento e vencimento entre 1 e 28.

Essas validações foram verificadas por meio de testes manuais em Python.

As funcionalidades de armazenamento no SQLite e comunicação HTTP ainda serão implementadas.

## 8. Como executar o teste manual

Com o Python instalado, abra o terminal na pasta principal do projeto.

Execute:

```powershell
python teste_manual_cartao.py
```

Esse comando executa os testes manuais iniciais da classe `Cartao`, desde que o arquivo tenha sido criado conforme as etapas de desenvolvimento.

Os testes automatizados com pytest serão implementados posteriormente.

## 9. Organização do desenvolvimento

O projeto será desenvolvido de maneira incremental, dividido em três Sprints.

- **Sprint 1:** cadastro de cartões de crédito.
- **Sprint 2:** registro de compras, parcelamento e organização de faturas.
- **Sprint 3:** despesas recorrentes e resumo financeiro mensal.

As decisões arquiteturais e os requisitos estão documentados no Relatório Técnico do projeto.

Os arquivos da pasta `docs/` serão utilizados como documentação complementar de apoio ao desenvolvimento.