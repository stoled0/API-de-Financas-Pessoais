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
- Os dias de fechamento e vencimento dos cartões devem estar entre 1 e 28.
- Não será permitido cadastrar cartões com nomes duplicados.
- Cartões com compras vinculadas poderão ter apenas seus nomes alterados e não poderão ser excluídos.
- Cada parcela de uma compra deverá possuir valor mínimo de R$ 0,01.

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

7. Situação atual do desenvolvimento

As cinco funcionalidades previstas no escopo estão implementadas: cadastro de cartões, registro de compras, parcelamento e organização de faturas, despesas recorrentes e resumo financeiro mensal.

O sistema utiliza três princípios SOLID (SRP, DIP e ISP) e quatro padrões de projeto GoF (Facade, Factory Method, Adapter e Template Method), além do padrão Repository para organização da persistência. A aplicação também conta com evidências de Desenvolvimento Orientado a Testes (TDD).

Resultados dos testes automatizados:
Total de testes: 86.
Testes aprovados: 86.
Falhas e erros: 0.
Cobertura geral do código: 95%.
Cobertura da camada de domínio: 93%.

As evidências de execução dos testes e os relatórios de cobertura estão disponíveis na pasta docs/testes/.

## 8. Como executar o projeto

### 8.1. Pré-requisitos

Para executar o projeto, é necessário possuir:

- Python instalado;
- Git instalado, caso o projeto seja obtido por meio da clonagem do repositório;
- Terminal ou ambiente de desenvolvimento, como o Visual Studio Code.

Não é necessário instalar um servidor de banco de dados, pois o projeto utiliza SQLite.

### 8.2. Instalação das dependências

Abra o terminal na pasta principal do projeto e execute:

```powershell
python -m pip install -r requirements.txt
```

Esse comando instalará as bibliotecas necessárias para a execução da API e dos testes automatizados.

### 8.3. Inicialização da API

Na pasta principal do projeto, execute:

```powershell
python -m uvicorn src.api.main:app --reload
```

Após a inicialização, a API estará disponível no endereço:

http://127.0.0.1:8000

### 8.4. Acesso à documentação interativa

Para acessar a documentação interativa do Swagger UI, abra o seguinte endereço no navegador:

http://127.0.0.1:8000/docs

Por meio dessa interface, será possível consultar as rotas disponíveis, enviar requisições e testar as funcionalidades implementadas:

- Cadastro e gerenciamento de cartões de crédito;
- Registro e consulta de compras;
- Geração de parcelas e consulta de faturas;
- Cadastro e consulta de despesas recorrentes;
- Consulta do resumo financeiro mensal.

Para encerrar a execução da API, pressione `Ctrl + C` no terminal.

### 8.5. Execução dos testes automatizados

Para executar todos os testes automatizados do projeto, utilize:

```powershell
python -m pytest -v
```

Caso deseje visualizar apenas o resultado resumido dos testes, execute:

```powershell
python -m pytest -q
```

Os testes contemplam as regras de negócio, a integração entre os componentes, as requisições HTTP, os contratos, a injeção de dependências, os padrões de projeto e a regra desenvolvida por meio do TDD.

### 8.6. Verificação da cobertura dos testes

Para verificar a cobertura geral do código-fonte, execute:

```powershell
python -m pytest --cov=src --cov-report=term-missing -q
```

Para verificar especificamente a cobertura da camada de domínio, execute:

```powershell
python -m pytest --cov=src.dominio --cov-report=term-missing -q
```

Para gerar um relatório visual de cobertura em formato HTML, execute:

```powershell
python -m pytest --cov=src --cov-report=html:docs/testes/cobertura -q
```

Após a execução, o relatório poderá ser consultado abrindo o arquivo:

`docs/testes/cobertura/index.html`

### 8.7. Evidências dos testes

Os registros de execução dos testes automatizados, os relatórios de cobertura e as evidências da aplicação do Desenvolvimento Orientado a Testes (TDD) estão disponíveis na pasta:

`docs/testes/`

As evidências das etapas RED, GREEN e REFACTOR estão disponíveis especificamente na pasta:

`docs/testes/tdd/`

## 9. Organização do desenvolvimento

O projeto será desenvolvido de maneira incremental, dividido em três Sprints.

- **Sprint 1:** cadastro de cartões de crédito.
- **Sprint 2:** registro de compras, parcelamento e organização de faturas.
- **Sprint 3:** despesas recorrentes e resumo financeiro mensal.

As decisões arquiteturais e os requisitos estão documentados no Relatório Técnico do projeto.

Os arquivos da pasta `docs/` serão utilizados como documentação complementar de apoio ao desenvolvimento.