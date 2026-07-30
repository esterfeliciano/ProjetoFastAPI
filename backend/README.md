# Fast Zero — Loja com Carrinho, Produtos e Tarefas

API REST construída com FastAPI, com autenticação JWT, cadastro de usuários, catálogo de produtos, carrinho de compras com checkout via WhatsApp, e um módulo de gerenciamento de tarefas.

---

##  Tecnologias utilizadas

| Camada | Tecnologia | Para que serve |
|---|---|---|
| Framework web | **FastAPI** | Cria as rotas da API, valida dados automaticamente e gera documentação interativa |
| Servidor | **Uvicorn** | Roda a aplicação FastAPI |
| Validação de dados | **Pydantic v2** | Define os "contratos" de entrada e saída de cada rota (schemas) |
| Configuração | **Pydantic Settings** | Lê variáveis de ambiente (`.env`) de forma tipada |
| Banco de dados | **SQLite** | Banco relacional leve, em um único arquivo (`database.db`) |
| ORM | **SQLAlchemy 2.0** | Mapeia classes Python para tabelas do banco (models) |
| Migrações | **Alembic** | Versiona e aplica mudanças na estrutura do banco |
| Autenticação | **PyJWT** | Gera e valida os tokens de acesso (JWT) |
| Hash de senha | **pwdlib (argon2)** | Nunca guarda senha em texto puro — guarda o hash |
| Gerenciador de dependências | **Poetry** | Instala pacotes e gerencia o ambiente virtual |
| Automação de tarefas | **poethepoet (poe)** | Atalhos de comando: `poetry poe test`, `poetry poe serve`, etc. |
| Qualidade de código | **Ruff** | Lint + formatação automática do código |
| Testes | **Pytest + pytest-cov** | Testes automatizados e relatório de cobertura |

---

##  Arquitetura do projeto

O projeto segue o padrão **"package by feature"** (organização por funcionalidade, não por tipo técnico). Cada domínio de negócio tem sua própria pasta com tudo que é dela: rotas, schemas e models juntos.

```
backend/
├── src/
│   ├── app.py                    # Monta a aplicação e registra os routers
│   ├── config/
│   │   ├── database_settings.py  # Conexão com o banco (engine, sessão)
│   │   └── app_settings.py       # Reservado p/ configs gerais (CORS, etc.)
│   ├── users/
│   │   ├── router.py             # Rotas de cadastro, login, edição
│   │   ├── schemas.py            # Contratos de entrada/saída de usuário
│   │   ├── models.py             # Tabela `users` no banco
│   │   ├── security.py           # Hash de senha, geração/validação de JWT
│   │   └── cart/
│   │       ├── router.py         # Rotas do carrinho
│   │       ├── schemas.py
│   │       └── models.py         # Tabelas `carts` e `cart_items`
│   ├── products/
│   │   ├── router.py             # CRUD de produtos
│   │   ├── schemas.py
│   │   └── models.py             # Tabela `products`
│   └── tasks/
│       ├── router.py             # CRUD de tarefas (to-do list)
│       ├── schemas.py
│       └── models.py             # Tabela `tasks`
├── migrations/                   # Histórico de versões do banco (Alembic)
├── tests/                        # Testes automatizados, um arquivo por domínio
└── pyproject.toml                # Dependências e configuração das ferramentas
```

**Por que essa organização é mais fácil de manter:** se você for mexer em "produto", tudo que precisa está dentro de `products/` — não precisa abrir 4 pastas diferentes (uma de rotas, uma de models, uma de schemas) só pra fazer uma alteração.

---

##  Fluxo de uso da API

### 1. Cadastro e login

```
Usuário                          API
   │                              │
   ├── POST /users/ ─────────────▶│  cria a conta (senha vira hash)
   │◀──────────── 201 Created ────┤
   │                              │
   ├── POST /token ──────────────▶│  envia usuário + senha
   │◀──── 200 OK + access_token ──┤  recebe o "crachá" (JWT)
```

A partir daqui, toda rota protegida exige esse token no cabeçalho:
`Authorization: Bearer <token>`

### 2. Navegando no catálogo e comprando

```
Usuário                          API
   │                              │
   ├── GET /products/ ───────────▶│  lista produtos (pública, sem login)
   │◀──── 200 OK + lista ─────────┤
   │                              │
   ├── POST /cart/ (+ token) ────▶│  adiciona item ao carrinho
   │◀──── 201 Created ────────────┤
   │                              │
   ├── GET /cart/ (+ token) ─────▶│  vê o carrinho atual
   │◀──── 200 OK ─────────────────┤
   │                              │
   ├── POST /cart/checkout ──────▶│  finaliza o pedido
   │◀── link do WhatsApp ─────────┤  carrinho é esvaziado, e o link
   │                              │  já vem com a mensagem pronta
```

### 3. Gerenciando tarefas pessoais

```
Usuário                          API
   │                              │
   ├── POST /tasks/ (+ token) ───▶│  cria uma tarefa vinculada a ele
   │◀──── 201 Created ────────────┤
   │                              │
   ├── GET /tasks/?state=doing ──▶│  filtra tarefas por status
   │◀──── 200 OK ─────────────────┤
   │                              │
   ├── PATCH /tasks/{id} ────────▶│  atualiza status/campos
   │◀──── 200 OK ─────────────────┤
```

Importante: cada usuário só enxerga e edita as **próprias** tarefas — a rota sempre filtra por `user_id` usando o usuário autenticado no token.

---

## O que cada rota faz

### Usuários (`/users`, `/token`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/users/` | POST | Cria uma nova conta | Não |
| `/users/` | GET | Lista todos os usuários | Não |
| `/users/{id}` | PUT | Edita os próprios dados | Sim (só o dono) |
| `/users/{id}` | DELETE | Apaga a própria conta | Sim (só o dono) |
| `/token` | POST | Faz login e retorna o token JWT | Não |

### Produtos (`/products`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/products/` | POST | Cadastra um novo produto | Sim |
| `/products/` | GET | Lista produtos (com paginação) | Não |
| `/products/{id}` | GET | Detalhe de um produto | Não |
| `/products/{id}` | PUT | Atualiza um produto | Sim |
| `/products/{id}` | DELETE | Remove um produto | Sim |

### Carrinho (`/cart`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/cart/` | POST | Adiciona um item ao carrinho | Sim |
| `/cart/` | GET | Mostra o carrinhho atual | Sim |
| `/cart/checkout` | POST | Fecha o pedido e gera link do WhatsApp | Sim |

### Tarefas (`/tasks`)
| Rota | Método | O que faz | Precisa de login? |
|---|---|---|---|
| `/tasks/` | POST | Cria uma tarefa | Sim |
| `/tasks/` | GET | Lista tarefas (com filtros) | Sim |
| `/tasks/{id}` | PATCH | Atualiza campos da tarefa | Sim |
| `/tasks/{id}` | DELETE | Remove a tarefa | Sim |

---

## Como funciona a segurança

1. A senha nunca é salva como texto puro — vira um **hash** (via `pwdlib`/argon2) antes de ir pro banco.
2. No login, a API gera um **token JWT** com validade de 30 minutos, contendo o e-mail do usuário criptografado dentro dele.
3. Toda rota protegida usa `Depends(get_current_user)`, que:
   - Lê o token enviado no cabeçalho
   - Decodifica e confere se não expirou
   - Busca o usuário correspondente no banco
   - Se algo falhar, retorna erro 401 (não autorizado)

---

## Como rodar o projeto

```bash
# instalar dependências
poetry install

# ativar o ambiente virtual
poetry env activate
# (copia e cola o comando "source .../activate" que aparecer)

# aplicar as migrações no banco
alembic upgrade head

# rodar os testes
poetry poe test

# subir o servidor
poetry poe serve
```

Depois, acesse `http://127.0.0.1:8000/docs` para testar todas as rotas na documentação interativa (Swagger UI).