# ADR-001 — Escolha do SQLite como banco de dados

**Status:** Aceito

## 1. Contexto

A API de Finanças Pessoais precisa armazenar informações de cartões de crédito, compras, parcelas e despesas recorrentes.

Como o projeto possui finalidade acadêmica e será desenvolvido por uma equipe com experiência inicial em desenvolvimento de APIs, buscamos uma solução que permita implementar e testar a persistência de dados sem exigir uma infraestrutura complexa.

## 2. Decisão

Utilizar o **SQLite** como banco de dados relacional do sistema.

O SQLite permite armazenar os dados em um arquivo local e pode ser utilizado diretamente com Python por meio da biblioteca `sqlite3`.

O acesso ao banco será organizado na camada de persistência, utilizando o padrão Repository para separar as operações de armazenamento das regras de negócio.

## 3. Alternativas consideradas

**MySQL/MariaDB:** bancos de dados relacionais adequados para aplicações com múltiplos usuários e operações simultâneas. Entretanto, sua utilização exige acesso a um servidor de banco de dados, configuração de conexão e instalação de um conector apropriado no Python.

Caso a API seja executada em outro computador, será necessário instalar e configurar um servidor local ou disponibilizar um servidor remoto acessível. Isso aumenta as etapas necessárias para executar o projeto em diferentes ambientes.

**SQLite:** banco de dados relacional que funciona diretamente com Python por meio da biblioteca `sqlite3`, disponível na instalação padrão da linguagem.

Não exige um servidor de banco de dados separado e permite armazenar as informações em um arquivo local, simplificando a configuração, os testes e a execução da API em diferentes computadores.

## 4. Consequências

**Vantagens:**

- Não exige instalação ou configuração de um servidor de banco de dados separado.
- Utiliza a biblioteca `sqlite3`, incluída na instalação padrão do Python.
- Permite criar automaticamente o arquivo do banco e suas tabelas durante a inicialização do sistema.
- Facilita a execução da API em diferentes computadores, inclusive durante a apresentação acadêmica.
- Oferece suporte a comandos SQL, relacionamentos e integridade referencial.
- Permite que a equipe concentre seus esforços nas funcionalidades, regras de negócio e testes.

**Limitações:**

- Possui limitações para cenários com muitas operações de escrita simultâneas, pois permite apenas uma operação de escrita por vez.
- Não é a opção mais adequada para aplicações com alta demanda de gravações concorrentes.
- O banco de dados é armazenado em um arquivo local, exigindo cuidados com armazenamento, permissões e cópias de segurança.
- Não oferece, por padrão, os mesmos recursos de administração centralizada de bancos de dados com servidor.
- Sua utilização não elimina a necessidade de instalar Python e as dependências da API no computador em que o sistema será executado.
- O acesso ao Swagger UI depende de a API estar em execução e acessível pela rede.

## 5. Justificativa

O SQLite foi escolhido por atender às necessidades funcionais da API de Finanças Pessoais e reduzir a complexidade de configuração do ambiente.

Como o projeto será desenvolvido e apresentado em contexto acadêmico, consideramos importante que ele possa ser executado em diferentes computadores sem exigir a instalação de um servidor MySQL ou MariaDB.

Com o SQLite, será necessário configurar o Python e instalar as dependências da aplicação, mas não haverá necessidade de configurar um servidor de banco de dados separado.

A decisão também considera que o sistema possui escopo limitado e não foi projetado para atender a um grande volume de usuários realizando gravações simultâneas.

O acesso aos dados será organizado pelo padrão Repository, mantendo as regras financeiras separadas dos comandos SQL e facilitando uma possível substituição futura do banco de dados.

Portanto, a escolha prioriza simplicidade de execução, portabilidade e adequação aos objetivos acadêmicos, reconhecendo as limitações do SQLite em cenários de maior concorrência.