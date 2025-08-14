# E-Shop Brasil — CRUD com MongoDB, Streamlit e Docker

Aplicação simples para gerenciar dados (CRUD) usando **MongoDB** como banco NoSQL, **Python** + **Streamlit** como interface e **Docker**/**docker-compose** para orquestração.
Inclui um **script de carga** com `Faker` que insere **+1 milhão de documentos** no MongoDB de forma eficiente (em lotes).

---

## 🚀 Stack
- Python 3.11
- Streamlit
- Pymongo (MongoDB driver)
- Docker + docker-compose
- Faker (geração de dados sintéticos)

---

## 📁 Estrutura
```
eshop-brasil-nosql-crud/
├─ app.py                 # Interface Streamlit (CRUD)
├─ db.py                  # Conexão e utilitários p/ MongoDB
├─ seed_data.py           # Geração de >1M registros com Faker
├─ requirements.txt       # Dependências Python
├─ Dockerfile             # Build do container da aplicação
├─ docker-compose.yml     # Orquestração (MongoDB + App)
├─ .env.example           # Variáveis de ambiente (exemplo)
└─ README.md
```

---

## ⚙️ Pré-requisitos
- Docker e docker-compose instalados
- (Opcional) Python 3.11+ se quiser rodar localmente sem container

---

## 🔧 Configuração (com Docker)
1) Copie o `.env.example` para `.env` (opcional — os defaults já funcionam):
```bash
cp .env.example .env
```

2) Suba os serviços (MongoDB + App):
```bash
docker compose up -d --build
```

3) A primeira vez pode demorar um pouco por conta do build da imagem.  
A aplicação Streamlit ficará acessível em http://localhost:8501  
O MongoDB expõe a porta `27017` no host.

---

## 🧪 Popular o banco com +1 milhão de documentos
O script usa inserção em lotes para performance.

Exemplo: 1.000.000 documentos, em lotes de 50.000:
```bash
docker compose run --rm app python seed_data.py --n 1000000 --batch 50000
```

Parâmetros:
- `--n` quantidade total de documentos (default: 1_000_000)
- `--batch` tamanho do lote (default: 50_000)
- `--collection` nome da coleção (default: customers)

O script cria **índices** úteis (por exemplo: `email`, `city`, `created_at`).

---

## 🖱️ Como usar a interface (CRUD)
1) Abra http://localhost:8501
2) Use o menu lateral para escolher a operação:
   - **Create** (criar novo registro)
   - **Read** (listar e filtrar com paginação)
   - **Update** (editar um registro existente pelo _id)
   - **Delete** (remover pelo _id)

Você pode filtrar por `nome`, `email`, `cidade` e faixa de datas de criação.

---

## 🧩 Variáveis de ambiente
Veja `.env.example`:
```
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=eshop
MONGO_URI=mongodb://mongo:27017
DEFAULT_COLLECTION=customers
```

---

## 📹 Entregável (vídeo sugerido)
1) `docker compose up -d --build`
2) Mostrar containers rodando: `docker compose ps`
3) Rodar o seed: `docker compose run --rm app python seed_data.py --n 1000000 --batch 50000`
4) Abrir o Streamlit (http://localhost:8501) e demonstrar CRUD (Create, Read, Update, Delete)
5) Mostrar a coleção no MongoDB (índices e contagem de documentos)
6) Encerrar com `docker compose down`

---

## 📦 Subir para o GitHub
1) Crie um repositório vazio no GitHub
2) No diretório do projeto:
```bash
git init
git add .
git commit -m "E-Shop Brasil: CRUD MongoDB + Streamlit + Docker (+1M dados Faker)"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
git push -u origin main
```

---

## 🧰 Dicas de performance
- Use **lotes grandes** (`--batch 50000` a `100000`) para inserir mais rápido.
- Evite criar índice **antes** de inserir dados massivos (o script cria após a carga inicial quando necessário).
- Prefira filtros que usem índices (`email`, `city`, `created_at`).
- Limite o número de colunas mostradas na UI para listas longas.

---

## 📃 Licença
MIT
