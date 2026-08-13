# DeepSearch Agent

DeepSearch Agent is an AI research agent built on Claude (Anthropic) and the Tavily search API. It is currently in early scaffolding: the configuration layer is in place and the agent logic is not yet implemented.

> School project — BTS SIO, Lycée Gustave Eiffel (Bordeaux).

## Status

This repository currently contains only the `backend` service scaffold:

- A typed, environment-based configuration module (`backend/core/config.py`).
- An entry point (`backend/main.py`) that loads config on startup; agent logic is not yet implemented.

## Tech stack

- **Python 3.12** (see `backend/.python-version`)
- **[uv](https://docs.astral.sh/uv/)** for dependency management (`backend/pyproject.toml`, `backend/uv.lock`)
- **Pydantic** / **pydantic-settings** for typed, environment-driven configuration

## Project structure

```
DeepSearch-Agent/
├── .env                  # local environment variables (not committed)
├── .env.example          # template for required environment variables
└── backend/
    ├── core/
    │   └── config.py     # AppConfig: loads and validates settings from .env
    ├── main.py           # entry point, loads config on startup
    ├── pyproject.toml    # backend dependencies
    └── uv.lock
```

## Configuration

Settings are loaded via `pydantic-settings` from a single `.env` file at the **repository root** (this is resolved automatically relative to `config.py`, regardless of which directory you run commands from).

Copy the template and fill in real values:

```bash
cp .env.example .env
```

| Variable            | Type   | Description                                      |
| -------------------- | ------ | ------------------------------------------------- |
| `MODEL_NAME`         | string | Claude model identifier to use for the agent      |
| `ANTHROPIC_API_KEY`  | secret | API key for the Anthropic (Claude) API            |
| `TAVILY_API_KEY`     | secret | API key for the Tavily search API                 |
| `MAX_ITERATIONS`     | int    | Maximum number of agent loop iterations per query  |
| `CACHE_TTL`          | int    | Cache time-to-live, in seconds                     |
| `PORT`               | int    | Port the backend service listens on                |
| `API_KEY`            | secret | API key clients must use to authenticate with this service |
| `ENVIRONMENT`        | string | Runtime environment (e.g. `development`, `production`) |

All fields are required — the app will fail to start if any are missing from `.env`.

Secret fields (`ANTHROPIC_API_KEY`, `TAVILY_API_KEY`, `API_KEY`) are typed as `SecretStr`. **Never log, print, or otherwise expose their raw values** — not in application logs, error messages, or debug output. If you need to confirm a key is loaded, log its presence (e.g. `bool(config.api_key)`) or a redacted form, never `config.api_key.get_secret_value()`.

## Getting started

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
cd backend
uv sync
```

Create your `.env` file at the repository root as described above, then run:

```bash
cd backend
uv run python main.py
```

## Roadmap

The following are referenced by the configuration but not yet implemented:

- Agent orchestration loop (Claude + Tavily search, bounded by `MAX_ITERATIONS`)
- Response/result caching (`CACHE_TTL`)
- HTTP API server exposing the agent (`PORT`, `API_KEY` for auth)
