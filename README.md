# Controle Financeiro Compartilhado

Sistema de controle financeiro pessoal e compartilhado, com foco em **compras parceladas no cartão de crédito**, **faturas por cartão** e **divisão de gastos entre pessoas**.

Trabalho Final da disciplina de Engenharia de Software — IFMG, Campus Ribeirão das Neves.
Sistema nº 12 da lista do professor: *API de Finanças Pessoais*.

## O problema

O sistema nasceu de uma planilha real de controle financeiro, que ficou complexa demais para usar no dia a dia:

- difícil de preencher pelo celular;
- fórmulas importantes podem ser apagadas por engano;
- corrigir um lançamento exige apagar células soltas;
- muitas abas e informações, o que dificulta a análise;
- quem tem pouco tempo ou pouca familiaridade com planilhas desiste de usar.

O sistema guarda as regras no código, testadas e protegidas: o usuário informa só o essencial e o resto é calculado.

## Funcionalidades do MVP

- Registro de compras à vista, parceladas e recorrentes
- Cálculo automático de parcelas e da fatura em que cada uma cai
- Divisão de gastos entre pessoas (rateio)
- Resumo mensal: recebido × gasto × saldo
- Alertas de orçamento por categoria
- Importação da planilha antiga (formato simplificado)

## Tecnologias

| Uso | Ferramenta |
| --- | --- |
| Linguagem | Python 3.12+ |
| API web | FastAPI (documentação OpenAPI automática) |
| Banco de dados | SQLite |
| Testes e cobertura | pytest + pytest-cov |
| Análise estática | Ruff (e SonarQube Cloud) |
| Integração contínua | GitHub Actions |
| Diagramas | PlantUML (somente UML) |

## Arquitetura

Arquitetura **hexagonal simplificada** (portas e adaptadores): as regras de negócio ficam no centro e não dependem de banco, web ou arquivos. Detalhes e justificativa nos ADRs em `docs/adr/`.

```
src/
  dominio/       regras de negócio puras (Lancamento, Parcela, Fatura...)
  aplicacao/     casos de uso e portas (interfaces)
  adaptadores/   API, banco SQLite, importador de planilha
tests/           testes unitários e de integração
  fixtures/      dados de teste ANONIMIZADOS
docs/
  requisitos/    histórias de usuário e requisitos não funcionais
  casos-de-uso/  descrições dos casos de uso
  uml/           diagramas (arquivos .puml)
  adr/           registros de decisões de arquitetura
  ia/            registro de uso de IA
```

## Como executar, testar e analisar

> Será preenchido na Sprint 1, quando o código inicial existir.

## Estratégia de branches (trunk-based)

- A branch `main` é a principal e está **protegida**: ninguém envia código direto para ela.
- Cada tarefa é feita em uma branch curta, criada a partir da `main`:
  - `feature/...` nova funcionalidade (ex.: `feature/parcelamento`)
  - `fix/...` correção de erro
  - `test/...` novos testes
  - `docs/...` documentação
- A branch volta para a `main` por **pull request**, com **1 aprovação de outro integrante**.
- **Ninguém aprova o próprio pull request.**
- Entregas marcadas com tags: `v0.1.0`, `v0.2.0` (apresentação parcial) e `v1.0.0` (entrega final).

O passo a passo e o padrão de mensagens de commit estão em [CONTRIBUTING.md](CONTRIBUTING.md).

## Equipe

| Integrante | Funcionalidade | Papel transversal |
| --- | --- | --- |
| *(cada integrante adiciona sua linha no primeiro pull request)* | | |

## Proteção de dados

Este repositório **não contém dados reais**. Planilhas e bancos de dados estão bloqueados no `.gitignore`. Os testes usam apenas dados fictícios em `tests/fixtures/`.

## Uso de inteligência artificial

O uso de IA neste projeto é declarado, conforme a seção 5 do enunciado. O registro de prompts, ferramentas e revisões fica em [docs/ia/registro-de-prompts.md](docs/ia/registro-de-prompts.md).
