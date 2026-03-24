# Implementation Summary

This project was updated to add API-key authentication, global exception handling, and async integration tests.

## What was added in `main.py`

- API-key header auth using FastAPI's `APIKeyHeader`:
  - header name: `X-API-Key`
  - valid key: `your-secret-api-key`
  - rejects invalid or missing keys with HTTP 401 and `{"detail": "Invalid API Key"}`.

- Global exception handlers:
  - `StarletteHTTPException` handler:
    - 404 returns `{"detail": "Resource not found"}`
    - other HTTP errors preserve original detail.
  - `RequestValidationError` handler returns 422 with request validation errors.
  - generic `Exception` handler returns 500 with `{"detail": "Internal server error"}`.

- Added `/cause_error` endpoint to test 500 handling.

- Existing bot operations remain unchanged (CRUD on `/items`).

## What was changed in `test_main.py`

- Switched to `httpx.AsyncClient` integration tests with `pytest.mark.asyncio`.
- Covered:
  - root access (200)
  - valid API key access (items read)
  - invalid API key access (401)
  - missing item (404)
  - validation failure (422)
  - forced internal error (500)

## How to run tests

1. Activate venv: `& .venv\Scripts\Activate.ps1`
2. Run: `pytest -q`

## Additional notes

- API-key enforcement is applied to all item endpoints and error endpoint.
- If desired, key lookup logic can be migrated from hard-coded `VALID_API_KEY` to database/secret store.
