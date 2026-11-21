# ADR-002 — Escolha do FastAPI para desenvolvimento da API

**Status:** Aceito

## 1. Contexto

A API de Finanças Pessoais precisa disponibilizar funcionalidades para cadastrar cartões de crédito, registrar compras, organizar parcelas e consultar informações financeiras.

Como o sistema será desenvolvido em Python e não terá uma interface gráfica própria, é necessário utilizar uma ferramenta que permita receber requisições HTTP, processar as solicitações e retornar respostas estruturadas.

Também buscamos uma solução que facilite a validação de dados, a documentação das funcionalidades e a realização de testes.

## 2. Decisão

Utilizar o **FastAPI** como framework para desenvolver a API REST do sistema.

O FastAPI será responsável por receber as requisições HTTP, encaminhar as operações para a camada de aplicação e retornar as respostas.

A ferramenta também disponibiliza documentação interativa por meio do Swagger UI, permitindo testar os endpoints (endereço específico da API que permite realizar determinada operação) diretamente pelo navegador.

## 3. Alternativas consideradas

**Flask:** framework Python que permite desenvolver aplicações web e APIs com flexibilidade e estrutura inicial simples. Entretanto, algumas funcionalidades, como validação estruturada de dados e documentação interativa, normalmente exigem bibliotecas adicionais.

**FastAPI:** framework Python voltado ao desenvolvimento de APIs, com recursos integrados de validação, documentação automática e definição de endpoints.

## 4. Consequências

**Vantagens:**

- Facilidade para criar endpoints HTTP.
- Validação de dados com recursos integrados.
- Geração automática de documentação interativa.
- Integração com Python.
- Facilidade para realizar testes das rotas.

**Limitações:**

- Necessidade de aprender os conceitos específicos do framework.
- Dependência de bibliotecas externas para executar a API.
- Necessidade de organizar corretamente as camadas para evitar que regras de negócio fiquem concentradas nas rotas.

## 5. Justificativa

O FastAPI foi escolhido por oferecer recursos adequados às necessidades da API de Finanças Pessoais, facilitando o desenvolvimento, a documentação e os testes.

Sua utilização também permite concentrar as regras financeiras nas camadas de domínio e aplicação, mantendo a camada de API responsável pela comunicação HTTP.