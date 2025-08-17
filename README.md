# CatInfo — LangChain/LangGraph + FastAPI (Docker-ready)

A small, production-ready FastAPI service that extracts and serves rich information about cat breeds using **TheCatAPI**, with a simple LangChain/LangGraph pipeline for enrichment and routing. The project uses a clean **`src/` layout**, is testable with **pytest** and fully containerized with **Docker**.

---

## 🔧 Tech Stack

* **Python 3.11/3.12**
* **FastAPI** + **Uvicorn**
* **Requests** (HTTP client)
* **LangChain** / **LangGraph** (simple enrichment pipeline)
* **pytest** (tests)
* **uv** (dependency + venv manager) — optional
* **Docker** (containerization)

---

## 📁 Project Structure

```
rpcats/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── src/
│   └── catinfo/
│       ├── __init__.py
│       ├── app.py              # FastAPI app (ASGI)
│       ├── main.py             # Optional CLI entry (argparse)
│       ├── utils.py            # Core logic: fetch, filter, summarise
│       ├── lang_module.py      # LangChain chain(s)
│       └── langgraph_module.py # LangGraph graph(s)
└── tests/
    ├── __init__.py
    └── test_utils.py
```

> **Why `src/` layout?** It avoids accidental imports from the working directory and matches modern packaging best practices.

---

## 🚀 Quickstart (Local, no Docker)

### 1) Create env & install deps (with `uv`)

```bash
# from repo-root
uv venv
uv pip install -r requirements.txt
```

(Or using `uv add <pkg>` to manage deps and `uv pip freeze > requirements.txt` to pin.)

### 2) Run FastAPI (Uvicorn)

Pick one of the following approaches.

**A. Preferred canonical import (set `PYTHONPATH`)**

```bash
# Linux/Mac
export PYTHONPATH=src
uv run uvicorn catinfo.app:app --reload --reload-dir src/catinfo

# Windows PowerShell
$env:PYTHONPATH = "src"
uv run uvicorn catinfo.app:app --reload --reload-dir src/catinfo
```

**B. Alternative (module path that includes `src` in the dotted name)**

```bash
uv run uvicorn src.catinfo.app:app --reload
```

> Use **either** A or B. A is cleaner long‑term; B works if your tools expect `src.` prefix.

### 3) Open the docs

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc:       [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testing

```bash
uv run pytest -q
```

Common import fixes during testing:

* Ensure `src/catinfo/__init__.py` exists.
* Run pytest **from repo root** (same folder as `src/` and `tests/`).
* If needed, set `PYTHONPATH=src` as shown above.

---

## 🧰 Development Commands (uv)

Add dependencies:

```bash
uv add fastapi uvicorn requests langchain langgraph python-dotenv pydantic
uv add --dev pytest
```

Export a simple `requirements.txt` (no editable `-e`):

```bash
# Make sure your package isn’t installed editable when freezing
uv pip uninstall -y catinfo  # if installed as -e
uv pip install ./src         # normal install
uv pip freeze > requirements.txt
```

> If `uv export` adds extra metadata you don’t want, prefer `pip freeze` for `name==version` lines only.

---

## 🌐 Environment Variables (.env)

Create a `.env` in the repo root (optional but recommended):

```
CAT_API_BASE=https://api.thecatapi.com/v1
CAT_API_KEY=your_key_if_you_have_one
LOG_LEVEL=info
```

Your code can load this via `python-dotenv` or FastAPI settings.

---

## 🧠 LangChain / LangGraph (minimal examples)

* `lang_module.py`: Define a simple chain that takes the raw breed JSON and produces a friendly summary (e.g., extract temperament, lifespan, origin, plus a compact description).
* `langgraph_module.py`: Route user intent (e.g., lookup by breed name vs. list vs. filter by origin) and call the appropriate node (API fetch → summarise).

These modules are optional; the app works without them, but they demonstrate how to plug LLM-style or graph-style steps into the pipeline.

---

## 🗺️ API Endpoints (example)

Assuming your `app.py` exposes something like:

* `GET /health` → Health check
* `GET /breeds` → Full list from TheCatAPI (cached or proxied)
* `GET /breeds/{name}` → Single breed, by human‑readable name (case‑insensitive)
* `GET /breeds/{name}/summary` → Enriched summary via LangChain

### Example requests

```bash
curl http://127.0.0.1:8000/breeds
curl http://127.0.0.1:8000/breeds/Siamese
curl http://127.0.0.1:8000/breeds/Siamese/summary
```

---

## 🐳 Docker (Production‑oriented)

**Dockerfile** (works with `src/` layout):

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Make sure Python can find the package under src/
ENV PYTHONPATH=/app

# Expose port (platforms like Render/Railway override via $PORT)
ENV PORT=8000

# Start the ASGI server
CMD ["uvicorn", "src.catinfo.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

> If you prefer the canonical import (no `src.` in dotted path), set `ENV PYTHONPATH=/app/src` and change the CMD to `"catinfo.app:app"`.

### Build & Run

```bash
# Build
docker build -t catinfo-app .

# Run locally
docker run --rm -p 8000:8000 catinfo-app

# Test inside container (optional)
docker run --rm -e PYTHONPATH=/app catinfo-app python -c "import src.catinfo as m; print(m.__file__)"
```

**Common Docker gotchas**

* `ModuleNotFoundError: No module named 'catinfo'` → Ensure `__init__.py` exists; set `PYTHONPATH` properly; confirm CMD uses the right dotted path.
* If you see *editable install* noise (`-e`), avoid `pip install -e ./src` in production images and rely on `requirements.txt` + `pip install ./src` (or just import via `PYTHONPATH`).

---

## 🧱 Packaging Notes (setuptools)

Minimal `pyproject.toml` for `src/` layout:

```toml
[project]
name = "rpcats"
version = "0.1.0"
description = "Display cat information for the specified breed."
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.116.1",
    "langchain>=0.3.27",
    "langgraph>=0.6.4",
    "requests>=2.32.4",
    "uvicorn>=0.35.0",
]

[dependency-groups]
dev = [
    "black>=25.1.0",
    "flake8>=7.3.0",
    "isort>=6.0.1",
    "pytest>=8.4.1",
]

[tool.setuptools.packages.find]
where = ["src"]
include = ["api", "app", "config", "langgraph_module", "lang_module", "main", "utils"]

[project.scripts]
rpcats = "main:main"

[build-system]
requires = ["setuptools>=78.1.0", "wheel>=0.45.1"]
build-backend = "setuptools.build_meta"
```

> If you do want to `pip install ./src`, add `__init__.py` and ensure your package name in `[project]` matches the import (`catinfo`).

---

## 🧯 Troubleshooting

### Pytest can’t import modules

* Ensure `src/catinfo/__init__.py` exists.
* Run from repo root and/or set `PYTHONPATH=src`.
* Use absolute imports in tests: `from catinfo.utils import find_breed_info`.

### `uv add` / build errors like *Multiple top-level modules discovered*

* Caused by placing many `.py` files at repo root. **Fix:** move code under `src/catinfo/` and declare packages in `pyproject.toml` (see above).

### `error in 'egg_base' option` during install

* Remove custom `egg_base` from legacy configs, or ensure the folder exists; with `pyproject.toml` + `src/` layout you usually don’t need it.

### Docker `ModuleNotFoundError` on `catinfo`

* Use the provided Dockerfile and keep `ENV PYTHONPATH=/app` with `CMD ["uvicorn", "src.catinfo.app:app", ...]` **or** switch to `ENV PYTHONPATH=/app/src` with `CMD ["uvicorn", "catinfo.app:app", ...]`.

---

## 📜 License

MIT (see `LICENSE`).

---

## 🙋 FAQ

**Q: Do I need an API key for TheCatAPI?**
A: Public endpoints work without a key, but rate-limits are friendlier with a key. Put it into `.env` as `CAT_API_KEY` if you have one.

**Q: Where do LangChain/LangGraph fit?**
A: They live in `lang_module.py` and `langgraph_module.py`. The FastAPI endpoints can call these to enrich raw API data with concise summaries or to route between list/lookup/filter behaviors.

**Q: How do I disable reload in Docker?**
A: Use the provided CMD (no `--reload`) for production. Use `--reload` only for local dev.

---