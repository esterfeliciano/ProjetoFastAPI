# Laços & Cia 

Loja virtual de laços, tiaras e acessórios infantis. O projeto tem duas partes que trabalham juntas: um **backend** (a API, que guarda e organiza os dados) e um **frontend** (o site que o cliente e o lojista realmente veem e usam).

---

## O que esse projeto faz

- O **cliente** entra no site, vê o catálogo de produtos, coloca itens no carrinho e finaliza o pedido — tudo isso **sem precisar criar conta**.
- O **lojista** (dono da loja) faz login numa área separada pra cadastrar e remover produtos do catálogo.
- Quando o cliente finaliza a compra, o site gera um link pronto do **WhatsApp**, já com a lista de produtos e o total, pra ele mandar o pedido direto pro número da loja.

---

## Como as duas partes conversam

```
[ Cliente / Lojista no navegador ]
              │
              │  (o Frontend mostra as telas)
              ▼
        Frontend (Angular)
              │
              │  (pede/envia dados via internet)
              ▼
        Backend (FastAPI)
              │
              ▼
        Banco de dados (PostgreSQL)
```

O **frontend** é tudo que aparece na tela: o catálogo bonito, o carrinho, os botões. Ele não guarda nada sozinho — toda vez que precisa de uma informação (lista de produtos, por exemplo), ele pergunta pro backend.

O **backend** é quem realmente guarda e organiza os dados no banco, decide quem pode fazer o quê (só o lojista pode cadastrar produto, por exemplo), e responde as perguntas que o frontend faz.

---

## Backend (a API)

Construído em **Python**, com o framework **FastAPI**.

**O que ele guarda e controla:**
- Produtos (nome, descrição, preço, estoque, categoria)
- Carrinho de cada cliente (identificado por um código único gerado no navegador dele, sem precisar de cadastro)
- Contas de lojista (usuário e senha, com login protegido por token)

**Tecnologias principais:**
- **FastAPI** — cria as rotas da API (os "endereços" que o frontend chama pra pedir ou enviar dados)
- **PostgreSQL** — o banco de dados, onde tudo fica salvo de verdade
- **SQLAlchemy + Alembic** — organiza as tabelas do banco e controla as mudanças nelas ao longo do tempo
- **JWT** — o "crachá" digital que prova que o lojista está logado

**Como rodar:**
```bash
poetry install
poetry run alembic upgrade head
poetry poe serve
```
A API sobe em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

---

## Frontend (o site)

Construído em **Angular** (com TypeScript).

**O que ele mostra:**
- Página inicial de apresentação da loja
- Catálogo de produtos, com botão de adicionar ao carrinho
- Carrinho, com opção de remover item e finalizar pedido
- Formulário de cadastro de produto (só aparece pro lojista logado)
- Tela de login do lojista

**Como rodar:**
```bash
npm install
ng serve
```
O site abre em `http://localhost:4200` (precisa do backend rodando ao mesmo tempo, em outro terminal).

---

## Resumindo em uma frase

O **backend** é o "cérebro" que guarda e organiza tudo; o **frontend** é a "cara" que o cliente e o lojista realmente enxergam e usam — e os dois precisam estar rodando juntos pra loja funcionar de verdade.
