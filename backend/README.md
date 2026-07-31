# Fast Zero — Loja com Carrinho, Produtos e Tarefas (Backend)

API REST construída com FastAPI, com autenticação JWT para o lojista, catálogo de produtos, carrinho de compras público (sem login) com checkout via WhatsApp, e um módulo de tarefas (não utilizado pelo front atualmente).

---

## Tecnologias utilizadas

| Camada | Tecnologia | Para que serve |
|---|---|---|
| Framework web | **FastAPI** | Cria as rotas da API, valida dados automaticamente e gera documentação interativa |
| Servidor | **Uvicorn** | Roda a aplicação FastAPI |
| Validação de dados | **Pydantic v2** | Define os "contratos" de entrada e saída de cada rota (schemas) |
| Configuração | **Pydantic Settings** | Lê variáveis de ambiente (`.env`) de forma tipada |
| Banco de dados | **PostgreSQL** | Banco relacional, rodando em container Docker |
| ORM | **SQLAlchemy 2.0** | Mapeia classes Python para tabelas do banco (models) |
| Migrações | **Alembic** | Versiona e aplica mudanças na estrutura do banco |
| Autenticação | **PyJWT** | Gera e valida os tokens de acesso (JWT) do lojista |
| Hash de senha | **pwdlib (argon2)** | Nunca guarda senha em texto puro — guarda o hash |
| Gerenciador de dependências | **Poetry** | Instala pacotes e gerencia o ambiente virtual |
| Automação de tarefas | **poethepoet (poe)** | Atalhos de comando: `poetry poe test`, `poetry poe serve`, etc. |
| Qualidade de código | **Ruff** | Lint + formatação automática do código |
| Testes | **Pytest + pytest-cov** | Testes automatizados e relatório de cobertura |

---

## Arquitetura do projeto

O projeto segue o padrão **"package by feature"** (organização por funcionalidade, não por tipo técnico).

```
backend/
├── src/
│   ├── app.py                    # Monta a aplicação, registra CORS e os routers
│   ├── config/
│   │   └── database_settings.py  # Conexão com o banco (engine, sessão)
│   ├── users/
│   │   ├── router.py             # Rotas de cadastro, login, edição (lojista)
│   │   ├── schemas.py
│   │   ├── models.py              # Tabela `users`
│   │   ├── security.py            # Hash de senha, geração/validação de JWT
│   │   └── cart/
│   │       ├── router.py         # Rotas do carrinho — PÚBLICO (sem login)
│   │       ├── schemas.py
│   │       └── models.py         # Tabelas `carts` e `cart_items`
│   ├── products/
│   │   ├── router.py             # CRUD de produtos (leitura pública, escrita exige login)
│   │   ├── schemas.py
│   │   └── models.py
│   └── tasks/                    # Módulo de tarefas — não utilizado pelo front atual
│       ├── router.py
│       ├── schemas.py
│       └── models.py
├── migrations/                   # Histórico de versões do banco (Alembic)
├── tests/
└── pyproject.toml
```

---

## Decisão de arquitetura: carrinho sem login

Diferente do desenho inicial, o carrinho **não exige conta do cliente**. Só o lojista precisa fazer login (para cadastrar/editar/remover produtos). O carrinho identifica o cliente por um `session_id` (UUID) gerado no navegador e enviado no header `X-Session-Id` em toda requisição — sem necessidade de cadastro para comprar.

```
Cliente                          API
   │                              │
   ├── GET /products/ ───────────▶│  lista produtos (pública)
   │◀──── 200 OK ──────────────────┤
   │                              │
   ├── POST /cart/ (+ X-Session-Id) ▶  adiciona item ao carrinho
   │◀──── 201 Created ────────────┤
   │                              │
   ├── DELETE /cart/items/{id} ──▶│  remove um item específico
   │◀──── 200 OK ─────────────────┤
   │                              │
   ├── POST /cart/checkout ──────▶│  finaliza o pedido
   │◀── link do WhatsApp ─────────┤  carrinho é esvaziado
```

O lojista, separadamente, loga para gerenciar o catálogo:
```
Lojista                          API
   │                              │
   ├── POST /token ──────────────▶│  login (usuário + senha)
   │◀──── 200 OK + access_token ──┤
   │                              │
   ├── POST /products/ (+ Bearer) ▶  cadastra produto
   │◀──── 201 Created ────────────┤
   ├── DELETE /products/{id} ────▶│  remove produto
```

---

## O que cada rota faz

### Usuários / Lojista (`/users`, `/token`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/users/` | POST | Cria uma nova conta de lojista | Não |
| `/users/` | GET | Lista todos os usuários | Não |
| `/token` | POST | Login do lojista, retorna o JWT | Não |

### Produtos (`/products`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/products/` | GET | Lista produtos (com paginação) | Não |
| `/products/{id}` | GET | Detalhe de um produto | Não |
| `/products/` | POST | Cadastra um novo produto | Sim (lojista) |
| `/products/{id}` | PUT | Atualiza um produto | Sim (lojista) |
| `/products/{id}` | DELETE | Remove um produto | Sim (lojista) |

### Carrinho (`/cart`) — público, identificado por `X-Session-Id`
| Rota | Método | O que faz |
|---|---|---|
| `/cart/` | POST | Adiciona um item ao carrinho |
| `/cart/` | GET | Mostra o carrinho atual |
| `/cart/items/{item_id}` | DELETE | Remove um item específico do carrinho |
| `/cart/checkout` | POST | Fecha o pedido e gera link do WhatsApp |

### Tarefas (`/tasks`)
Módulo construído no início do projeto para prática de rotas/CRUD, **não integrado ao front da loja**. As rotas existem e exigem login, mas a tabela correspondente não está criada no banco de produção atual — considerar removido/fora de escopo.

---

## Como funciona a segurança

1. A senha do lojista nunca é salva como texto puro — vira um **hash** (via `pwdlib`/argon2).
2. No login, a API gera um **token JWT** válido por 30 minutos.
3. Toda rota de escrita de produto usa `Depends(get_current_user)`, que decodifica e valida o token. Token expirado ou inválido retorna `401 Unauthorized` (não mais erro 500).
4. As rotas de carrinho **não** usam autenticação — usam apenas o header `X-Session-Id` para isolar o carrinho de cada cliente.

---

## Como rodar o projeto

```bash
# instalar dependências
poetry install

# ativar o ambiente virtual
poetry env activate
# (copia e cola o comando "source .../activate" que aparecer)

# .env necessário na raiz do backend:
# DATABASE_URL="postgresql://usuario:senha@localhost:5432/nome_do_banco"

# aplicar as migrações no banco
poetry run alembic upgrade head

# rodar os testes
poetry poe test

# subir o servidor
poetry poe serve
```

Depois, acesse `http://127.0.0.1:8000/docs` para testar todas as rotas na documentação interativa (Swagger UI).

### Banco de dados (PostgreSQL via Docker)

Este projeto assume um PostgreSQL acessível em `localhost:5432`. Se estiver usando um container Docker existente, crie um banco e usuário dedicados:

```sql
CREATE DATABASE lojinha;
CREATE USER lojinha_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE lojinha TO lojinha_user;
\c lojinha
GRANT ALL ON SCHEMA public TO lojinha_user;
```

### CORS

O `app.py` libera especificamente `http://localhost:4200` (origem padrão do `ng serve`). Ajuste `allow_origins` se o front rodar em outra porta/domínio.

### WhatsApp

O número de destino do checkout está fixo em `src/users/cart/router.py`, na variável `numero_whatsapp`. Troque pelo número real da loja (formato: código do país + DDD + número, só dígitos).

---

## Próximos passos conhecidos

- Upload real de imagem de produto (hoje é um preview salvo apenas no `localStorage` do navegador do lojista)
- Papel/role de administrador explícito (hoje qualquer conta de usuário pode cadastrar produtos)
- Migração/limpeza do módulo de tarefas (tabela não criada em produção)
- Endereço de entrega, frete e pagamento automatizado (checkout atual é via link do WhatsApp)