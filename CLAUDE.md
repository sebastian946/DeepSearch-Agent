# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

DeepSearch Agent is an early-stage AI research agent intended to combine Claude (Anthropic) with the Tavily search API. Currently only the `backend` service scaffold exists: a validated configuration layer is in place, but the agent orchestration logic itself has not been implemented yet — `backend/main.py` is just an entry point that loads config on startup.

## Commands

All commands are run from `backend/` (it is a self-contained `uv` project with its own `pyproject.toml`/`uv.lock`/`.venv`, separate from the repo root).

```bash
cd backend
uv sync                  # install dependencies
uv run python main.py    # run the app
uv run ruff check .      # lint
```

There is no test suite yet.

## Architecture

- **Two-level repo layout**: the repo root holds the single `.env` file and top-level docs; all Python code and dependency management live under `backend/`, which is its own `uv`-managed project.
- **Config loading (`backend/core/config.py`)**: `AppConfig` (a `pydantic-settings` `BaseSettings`) is the single source of truth for runtime configuration. All fields are required (`Field()` with no default) so the app fails fast with a clear `ValidationError` listing every missing variable if `.env` is incomplete — don't add defaults to make fields optional unless that's an intentional product decision.
- **`.env` resolution is location-based, not CWD-based**: `_ROOT_ENV_FILE` in `config.py` is computed via `Path(__file__).resolve().parent.parent.parent / ".env"`, always pointing at the repo-root `.env` regardless of the working directory a command is run from. If `config.py` is ever moved, this relative depth must be updated accordingly.
- **Secrets are typed as `SecretStr`** (`anthropic_api_key`, `tavily_api_key`, `api_key`). Never log, print, or otherwise expose their raw values (including in error messages/debug output) — call `.get_secret_value()` only at the point of use (e.g. passing to an API client), never for logging. To confirm a key is loaded, log its presence/truthiness, not the value.
- Access config via `get_config()` in `backend/core/config.py`, not by instantiating `AppConfig()` directly elsewhere.
