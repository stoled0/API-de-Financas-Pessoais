# ADR-003 — Escolha da Arquitetura em Camadas

**Status:** Aceito

## 1. Contexto

A API de Finanças Pessoais precisa implementar diferentes funcionalidades, como cadastro de cartões, registro de compras, cálculo de parcelas, organização de faturas e controle de despesas recorrentes.

Essas funcionalidades envolvem comunicação HTTP, validação de informações, aplicação de regras financeiras e armazenamento de dados.

Para facilitar o desenvolvimento e a manutenção do sistema, precisamos organizar essas responsabilidades de maneira clara, evitando concentrar todas as operações em um único arquivo ou componente.

## 2. Decisão

Adotar uma **arquitetura em camadas**, organizada em quatro partes principais:

**Camada de API (`src/api`):**

Responsável por receber requisições HTTP, validar os dados de entrada no nível da interface e retornar respostas ao usuário.

**Camada de aplicação (`src/aplicacao`):**

Responsável por coordenar as funcionalidades, utilizando as regras de negócio e solicitando operações de persistência quando necessário.

**Camada de domínio (`src/dominio`):**

Responsável por representar os elementos financeiros e implementar as regras de negócio, como validação de cartões, cálculo de parcelas e determinação das faturas.

Essa camada não deverá depender diretamente do FastAPI ou do SQLite.

**Camada de persistência (`src/persistencia`):**

Responsável por armazenar e recuperar informações no banco de dados SQLite.

O acesso aos dados será organizado utilizando o padrão Repository, de modo que as regras financeiras não precisem conhecer os comandos específicos do banco de dados.

## 3. Alternativas consideradas

**Organização sem separação clara de camadas:**

Consiste em concentrar a comunicação HTTP, as regras financeiras e os comandos de banco de dados nos mesmos arquivos ou funções.

Embora possa facilitar a implementação de exemplos muito pequenos, essa organização tende a dificultar os testes, a manutenção e a identificação das responsabilidades conforme o sistema cresce.

**Arquitetura hexagonal (Ports and Adapters):**

Organiza o sistema em torno das regras de negócio, utilizando interfaces e adaptadores para conectar recursos externos, como APIs e bancos de dados.

Essa abordagem oferece boa separação de dependências, mas exige uma estrutura conceitual adicional que não foi considerada necessária para o escopo acadêmico simplificado.

**Arquitetura em camadas:**

Organiza o código por responsabilidades, facilitando a compreensão da estrutura e a separação entre comunicação HTTP, coordenação das operações, regras financeiras e armazenamento de dados.

## 4. Consequências

**Vantagens:**

- Separação clara das responsabilidades.
- Maior facilidade para localizar e modificar funcionalidades.
- Possibilidade de testar as regras financeiras sem depender diretamente do banco de dados ou da API.
- Melhor organização para o trabalho em equipe.
- Estrutura favorável à aplicação de princípios SOLID e padrões de projeto.

**Limitações:**

- Necessidade de criar e organizar mais módulos Python.
- Maior quantidade de arquivos em comparação com uma implementação concentrada em um único módulo.
- Necessidade de manter os limites entre as camadas para evitar dependências inadequadas.

## 5. Justificativa

A arquitetura em camadas foi escolhida por oferecer uma organização adequada ao tamanho e aos objetivos da API de Finanças Pessoais.

A separação entre API, aplicação, domínio e persistência permitirá desenvolver as funcionalidades gradualmente, facilitará a implementação de testes e contribuirá para demonstrar os princípios e padrões de projeto exigidos na disciplina.

Essa decisão também está alinhada à estrutura arquitetural apresentada no Capítulo 4 do Relatório Técnico.