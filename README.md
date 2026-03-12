# Lionel No IT — Documentação do MVP

Este projeto é um **MVP de assistente conversacional** com personalidade própria, construído com Flask e integração opcional com LLM local via Ollama.

## Visão geral

O Lionel No IT combina:
- **Regras fixas** (ex.: agenda da semana, nome do bot, criador, despedida);
- **Fallback com LLM** local (primeiro modelo menor, depois maior);
- **Fallback final randômico** caso os LLMs não estejam disponíveis.

A proposta do MVP é validar rapidamente:
1. experiência conversacional;
2. fluxo híbrido regra + IA;
3. operação local sem dependência obrigatória de nuvem.

---

## Arquitetura do MVP

- **Backend**: Flask (`Lionel no IT/app.py`)
- **Frontend**: template HTML (`Lionel no IT/templates/interface.html`)
- **LLM Gateway**: API local do Ollama (`http://localhost:11434/api/generate`)

Fluxo da requisição `POST /chat`:
1. valida payload;
2. tenta responder por regras;
3. se não houver regra, chama `gemma3:4b`;
4. se falhar, chama `mistral-nemo:12b`;
5. se tudo falhar, responde com frase aleatória de fallback.

---

## Estrutura de pastas

```text
.
├── Lionel no IT/
│   ├── app.py
│   └── templates/
│       └── interface.html
├── tests/
│   └── test_app.py
└── README.md
```

---

## Requisitos

- Python 3.10+
- Dependências Python:
  - `flask`
  - `requests`
  - `markdown`
- (Opcional, para respostas por IA) Ollama em execução com os modelos:
  - `gemma3:4b`
  - `mistral-nemo:12b`

### Instalação rápida

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask requests markdown
```

---

## Como executar

Na raiz do projeto:

```bash
python 'Lionel no IT/app.py'
```

Aplicação disponível em:
- `http://localhost:5000/`

---

## Endpoints da API

### `GET /`
Renderiza a interface web do chat.

### `GET /health`
Healthcheck simples.

**Resposta esperada**:
```json
{"status": "ok"}
```

### `POST /chat`
Processa a mensagem enviada pelo usuário.

**Body (JSON)**:
```json
{"mensagem": "qual aula na terca?"}
```

**Possíveis respostas**:
- `source: "regras"` → quando uma regra fixa resolve;
- `source: "llm_small"` → resposta vinda do `gemma3:4b`;
- `source: "llm_big"` → resposta vinda do `mistral-nemo:12b`;
- `source: "fallback"` → frase aleatória de fallback.

**Validação**:
- Retorna `400` se `mensagem` estiver vazia ou inválida.

---

## Regras implementadas no MVP

- Consulta de agenda por dia da semana;
- Reconhecimento com e sem acento (`terca/terça`, `sabado/sábado`);
- Perguntas sobre nome do bot;
- Pergunta sobre criador;
- Gatilho de calculadora;
- Mensagens de saída (`sair`, `tchau`, `bye`, `falou`).

---

## Testes

A suíte atual cobre:
- rejeição de mensagem vazia;
- detecção de dia sem acento;
- endpoint de healthcheck.

Executar:

```bash
python -m unittest discover -s tests -v
```

---

## Limitações conhecidas (MVP)

- Contadores em memória (resetam ao reiniciar a aplicação);
- Sem autenticação e sem persistência de histórico em banco;
- Dependência de LLM local para respostas mais abertas;
- Sem versionamento de prompts/model routing avançado.

---

## Próximos passos sugeridos

1. Persistência (SQLite/PostgreSQL) para histórico de chats;
2. Observabilidade (logs estruturados + métricas);
3. Configuração por variáveis de ambiente;
4. Tratamento de exceções com mensagens de erro mais claras;
5. Pipeline de CI com testes automatizados e lint;
6. Containerização com Docker.

---

## Licença

Sem licença definida até o momento.
