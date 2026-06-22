# Getting Started with OceanicOS

## Quick Start

### 1. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the server

```bash
python drop.py
```

The API will be available at `http://localhost:8000`.

## Using the Web UI

Visit `http://localhost:8000` to access the React dashboard.

- **Status**: View memory count and system status
- **Observe**: Send observations to the Drop

## API Endpoints

### GET /status
Returns the current Drop status and memory statistics.

```bash
curl http://localhost:8000/status
```

Response:
```json
{"name": "OneDrop", "memory_count": 10}
```

### POST /observe
Send observations to the Drop.

```bash
curl -X POST http://localhost:8000/observe \
  -H "Content-Type: application/json" \
  -d '{"source": "cli", "payload": {"msg": "hello"}}'
```

### POST /learn (optional)
Call a language model to learn from a prompt.

Requires `OPENAI_API_KEY` to be set.

```bash
curl -X POST http://localhost:8000/learn \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is OceanicOS?"}'
```

## Configuration

### Memory Backend

Switch between SQLite, JSON, and Chroma:

```bash
export MEMORY_BACKEND=json  # or sqlite, chroma
python drop.py
```

### API Key Protection

Require an API key for write endpoints:

```bash
export OCEANIC_API_KEY=your-secret-key
python drop.py
```

Then use the key in requests:

```bash
curl -H "X-API-KEY: your-secret-key" \
  http://localhost:8000/observe
```

### OpenAI Integration

Enable the `/learn` endpoint:

```bash
export OPENAI_API_KEY=sk-...
python drop.py
```

## Examples

See the `examples/` directory for sample workflows:

- `observe.py`: Simple async observation loop
- `api_client.py`: HTTP API client example

Run locally:

```bash
python examples/observe.py
python examples/api_client.py  # requires server running
```

## Docker

Build and run in Docker:

```bash
docker build -t oceanicos .
docker run -p 8000:8000 oceanicos
```

## Development

### Building the React dashboard

```bash
cd web
npm install
npm run build
```

The built UI will be served from `/` when you run the server.

### Running tests

```bash
pytest -q
```

### Running with auto-reload

```bash
pip install watchfiles
python -m uvicorn interfaces.api:app --reload
```

## Next Steps

- Explore the Chroma vector DB adapter for semantic memory
- Integrate local LLMs via `models/local_llm.py`
- Build custom workflows using the Drop core loop
- Extend memory adapters for your use case

## Architecture

OceanicOS follows the core loop:

```
Observe() → Remember() → Learn() → Create() → Steward() → Return()
```

Each layer is modular and can be extended independently.

---

💧 One Drop. Infinite Reflections.
