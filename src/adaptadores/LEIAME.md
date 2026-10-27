# Adaptadores: as conexões com o mundo de fora

Aqui fica tudo que conecta o sistema ao exterior:
- **entrada:** a API (FastAPI), que recebe os pedidos;
- **saída:** o banco de dados (SQLite) e o leitor da planilha antiga.

Cada adaptador de saída "encaixa" em uma porta definida em `src/aplicacao`. Trocar um adaptador (ex.: outro banco) não muda as regras do domínio.
