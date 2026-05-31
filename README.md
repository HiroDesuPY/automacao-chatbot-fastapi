# automacao-chatbot-fastapi

Projeto FastAPI que integra um bot Telegram, processamento de relatórios com LangChain/Ollama e armazenamento de embeddings no Pinecone. Possui rotas para upload de CSV que são processados, chunked e enviados para um vector store.

**Estrutura**

- `main.py` - Inicializa a aplicação FastAPI e dispara o bot em thread
- `config.py` - Carrega variáveis de ambiente
- `bot/` - Código do bot Telegram (`bot.py`)
- `services/` - Lógica de IA (`ia_langchain.py`, `pergunta_ia.py`)
- `uploads/` - Rota de upload e processamento CSV (`upload.py`)
- `Dockerfile`, `docker-compose.yml` - Containers para FastAPI, Postgres, Redis, Ollama
- `requirements.txt` - Dependências Python

## Requisitos

- Docker & Docker Compose (recomendado)
- ou Python 3.12+ e `venv` para desenvolvimento local

## Variáveis de ambiente

Crie um arquivo `.env` baseado em `.env.example` com os valores:

- `PINECONEAPI` - chave da sua conta Pinecone
- `TELEGRAMBOT_API` - token do bot Telegram
- `DATABASE_URL` - URL do Postgres (opcional se usar docker-compose)
- `REDIS_URL` - URL do Redis (opcional se usar docker-compose)
- `OLLAMA_HOST` - host do Ollama (ex: `http://localhost:11434`)

## Rodando com Docker Compose (recomendado)

1. Copie o `.env.example` para `.env` e ajuste valores:

```bash
cp .env.example .env
# editar .env com PINECONEAPI e TELEGRAMBOT_API
```

2. Subir os serviços:

```bash
docker compose up -d --build
```

3. Ver logs:

```bash
docker compose logs -f fastapi_app
```

4. Acessos:

- FastAPI: http://localhost:8000
- Docs: http://localhost:8000/docs
- Ollama: http://localhost:11434
- Redis: redis://localhost:6379
- Postgres: postgresql://admin:4225@localhost:5432/chatbot_db

## Rodando localmente (venv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# editar .env
uvicorn main:app --reload
```

Observação: o bot Telegram também é inicializado pelo `main.py` numa thread. Para o bot funcionar localmente, forneça `TELEGRAMBOT_API` válido e verifique conectividade com Redis/Pinecone/Ollama.

## Endpoints importantes

- `GET /` — verifica que a API está no ar (implementar conforme necessidade)
- `POST /upload/csv` — recebe um `multipart/form-data` com campo `file` (CSV). Exemplo `curl`:

```bash
curl -X POST "http://localhost:8000/upload/csv" -F "file=@/caminho/para/relatorio.csv"
```

Resposta esperada (sucesso): JSON com `status: success` e `message` com resultado do processamento.

## Bot Telegram

- O bot usa `pyTelegramBotAPI` (modo assíncrono). O token deve estar em `TELEGRAMBOT_API`.
- O bot processa mensagens criando uma instância `IA` (em `services/pergunta_ia.py`) que busca contexto no Pinecone e usa Ollama para gerar respostas.

## Observações técnicas e pontos de atenção

- O processamento de CSV gera um relatório via LLM (`ia_langchain.py`), então o container `ollama` deve estar disponível na porta `11434` ou ajustar `OLLAMA_HOST`.
- O projeto salva embeddings no Pinecone — configure `PINECONEAPI` e crie o índice `embeddinggemma-fastapi` se necessário.
- Redis é usado para histórico de conversas via LangChain (`RedisChatMessageHistory`). No `docker-compose.yml` o serviço Redis está mapeado na porta `6379`.
- Dependências LangChain e integrações podem ter mudanças de versão — se houver conflitos, ajuste `requirements.txt` e instale em ambiente virtual antes de construir a imagem.

## Debugging rápido

- Ver logs do FastAPI: `docker compose logs -f fastapi_app`
- Entrar no container Redis: `docker exec -it <redis_container> redis-cli`
- Testar endpoint de upload com `curl` acima

## Desenvolvimento

- Arquivos principais:
  - `uploads/upload.py` — ponto de entrada para processamento CSV
  - `services/ia_langchain.py` — gera relatório e cria chunks
  - `services/pergunta_ia.py` — busca contexto e monta prompt para responder perguntas
  - `bot/bot.py` — handler do Telegram

Se quiser, eu posso:

- Ajustar/normalizar dependências em `requirements.txt` para evitar conflitos
- Adicionar testes simples ou um script de exemplo para enviar um CSV de teste
- Configurar um `Makefile` ou `Make` targets para facilitar comandos comuns

---

Gerado automaticamente pelo assistente para orientar setup e uso do projeto.
