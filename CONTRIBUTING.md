# Guia de contribuição

Como trabalhar no repositório, do início ao fim de uma tarefa.

## 1. Antes de começar: atualize sua cópia

```
git switch main
git pull
```

## 2. Crie uma branch para a tarefa

```
git switch -c feature/nome-curto-da-tarefa
```

Prefixos: `feature/` (funcionalidade), `fix/` (correção), `test/` (testes), `docs/` (documentação), `refactor/` (melhoria interna), `ci/` (pipeline).

## 3. Trabalhe e faça commits pequenos

```
git add <arquivos>
git commit -m "tipo: descrição curta"
```

## 4. Envie e abra o pull request

```
git push -u origin feature/nome-curto-da-tarefa
```

No GitHub, clique em **Compare & pull request**, preencha o modelo e peça revisão a um colega.

## 5. Depois do merge

```
git switch main
git pull
```

---

## Padrão de mensagens de commit (Conventional Commits)

Formato: `tipo: descrição curta`, em português, no máximo 72 caracteres, sem ponto final.

| Tipo | Quando usar | Exemplo |
| --- | --- | --- |
| `feat` | Nova funcionalidade | `feat: calcula vencimento da fatura por cartão` |
| `fix` | Correção de erro | `fix: ajusta centavos na última parcela` |
| `test` | Testes novos ou alterados | `test: adiciona testes de rateio percentual` |
| `docs` | Documentação, UML, ADRs | `docs: adiciona diagrama de estados da fatura` |
| `refactor` | Melhoria interna sem mudar o comportamento | `refactor: extrai calculadora de parcelas` |
| `style` | Formatação, sem mudança de lógica | `style: aplica formatação do Ruff` |
| `ci` | Pipeline do GitHub Actions | `ci: adiciona etapa de cobertura` |
| `chore` | Tarefas gerais (configuração, dependências) | `chore: adiciona pytest às dependências` |

**Evidência de TDD:** o commit do teste vem **antes** do commit da implementação.

```
test: adiciona teste da soma das parcelas igual ao total
feat: implementa geração de parcelas em centavos
```

---

## Como revisar um pull request

1. Leia a descrição: o que mudou e por quê.
2. Veja as mudanças na aba **Files changed**.
3. Confira: o código é compreensível? Há testes? Os nomes batem com a UML?
4. Comente com respeito e de forma específica ("esta função faz duas coisas; separar?").
5. Aprove (**Approve**) ou peça ajustes (**Request changes**).

Revisar também conta como contribuição registrada no histórico.
