# Laços & Cia — Front-end (Angular)

Front-end da loja, construído em Angular (standalone components, zoneless, signals), integrado de verdade com o backend FastAPI — sem dados mockados.

---

## Tecnologias utilizadas

| Tecnologia | Para que serve |
|---|---|
| **Angular** (standalone, zoneless) | Framework front-end: componentes, rotas, formulários e HTTP |
| **TypeScript** | Linguagem tipada em que o Angular é escrito |
| **Signals** | Estado reativo do componente (obrigatório aqui, já que o projeto é zoneless) |
| **Reactive Forms** | Formulários com validação (login, cadastro de produto) |
| **HttpClient + Interceptor** | Chamadas à API, com anexação automática do token JWT do lojista |
| **Angular Router + Guard** | Navegação entre telas, com proteção de rotas restritas ao lojista |

---

## Estrutura

```
src/
├── app/
│   ├── app.ts / app.html / app.css        # Componente raiz: header, menu, router-outlet
│   ├── app.config.ts                       # Providers: router, HttpClient + interceptor
│   ├── app.routes.ts                       # Definição de rotas
│   ├── home/                               # Página inicial (apresentação da loja)
│   ├── product-list/                       # Catálogo (público) + ações do lojista
│   ├── product-form/                       # Cadastro de produto (restrito ao lojista)
│   ├── cart-view/                          # Carrinho (público)
│   ├── login/                              # Login do lojista
│   ├── services/
│   │   ├── product.ts                      # GET/POST/DELETE de produtos
│   │   ├── cart.ts                         # GET/POST/DELETE do carrinho + checkout
│   │   ├── cart-session.ts                 # Gera/persiste o session_id do cliente (localStorage)
│   │   ├── auth.ts                         # Login do lojista, guarda o JWT
│   │   └── product-image.ts                # Preview de foto de produto (local, temporário)
│   ├── interceptors/
│   │   └── auth-interceptor.ts             # Anexa "Authorization: Bearer <token>" quando logado
│   └── guards/
│       └── auth-guard.ts                   # Protege rotas que exigem login do lojista
```

---

## Decisões importantes

### Zoneless + Signals
O projeto usa `provideZonelessChangeDetection()`. Isso significa que **qualquer dado que chega de forma assíncrona** (respostas HTTP, timers) precisa estar em um `signal()` para que a tela atualize sozinha. Propriedades de classe simples (`this.produtos = [...]`) não disparam re-renderização nesse modo — funcionam apenas para mudanças síncronas (ex: dentro de um `(click)`).

### Quem loga, e quem não loga
- **Cliente**: nunca precisa de conta. O carrinho usa um `session_id` (UUID) gerado no primeiro acesso e salvo no `localStorage`, enviado no header `X-Session-Id` em toda chamada de carrinho.
- **Lojista**: loga para cadastrar/remover produtos. As rotas `/products/new` são protegidas por `authGuard` — sem token válido, o usuário é redirecionado para `/login`.

### Imagem de produto
O backend ainda não suporta upload de imagem. Como solução temporária, a foto (reduzida para uma miniatura antes de salvar) fica guardada no `localStorage` do navegador, associada ao `id` do produto. **Limitação conhecida**: a imagem não sincroniza entre navegadores/dispositivos, e produtos cadastrados antes dessa funcionalidade não têm foto retroativa.

---

## Como rodar

Pré-requisito: backend rodando em `http://127.0.0.1:8000` com CORS liberado para `http://localhost:4200`.

```bash
npm install
ng serve
```

Acesse `http://localhost:4200`.

### Ajustando a URL da API

A URL do backend está fixa como `http://127.0.0.1:8000` dentro de cada service que faz chamadas HTTP (`product.ts`, `cart.ts`, `auth.ts`). Se o backend rodar em outro endereço/porta, ajuste a constante `API_URL` em cada um desses arquivos.

### Criando o primeiro usuário lojista

Como não existe tela de cadastro no front (ainda), crie a primeira conta pelo Swagger do backend:
`http://127.0.0.1:8000/docs` → `POST /users/`.

---

## Próximos passos conhecidos

- Paginação no catálogo (o backend já aceita `skip`/`limit` via query string; o front ainda busca tudo de uma vez)
- Tela de cadastro do lojista dentro do próprio app
- Upload de imagem real (hoje é local/temporário — ver `product-image.ts`)
- Estados de carregamento/erro mais refinados nas telas