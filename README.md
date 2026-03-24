# API with Key Authentication

A FastAPI application that demonstrates API-key authentication via HTTP headers, global exception handlers, and integration tests using httpx.AsyncClient.

## Features

- **API Key Authentication**: Uses `X-API-Key` header for authentication
- **Global Exception Handlers**: Handles 404 (Not Found), 422 (Validation Error), and 500 (Internal Server Error)
- **CRUD Operations**: Basic Create, Read, Update, Delete operations for items
- **Integration Tests**: Comprehensive tests using httpx.AsyncClient

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Key

Use the following API key in the `X-API-Key` header:

```
your-secret-api-key
```

## API Endpoints

- `GET /` - Welcome message
- `GET /items/{item_id}` - Get item by ID
- `POST /items/` - Create new item
- `PUT /items/{item_id}` - Update item by ID
- `DELETE /items/{item_id}` - Delete item by ID

## Running Tests

Run the integration tests:

```bash
pytest test_main.py -v
```

## Example Requests

Get an item:

```bash
curl -H "X-API-Key: your-secret-api-key" http://127.0.0.1:8000/items/1
```

Create an item:

```bash
curl -X POST -H "X-API-Key: your-secret-api-key" -H "Content-Type: application/json" -d '{"name": "Test Item", "description": "A test item", "price": 10.0}' http://127.0.0.1:8000/items/
```
