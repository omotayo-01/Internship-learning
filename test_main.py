import pytest
import httpx
from main import app

VALID_API_KEY = "your-secret-api-key"
INVALID_API_KEY = "invalid-key"

@pytest.mark.asyncio
async def test_read_root():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

@pytest.mark.asyncio
async def test_read_item_with_valid_key():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1", headers={"X-API-Key": VALID_API_KEY})
    assert response.status_code == 200
    assert "name" in response.json()

@pytest.mark.asyncio
async def test_read_item_with_invalid_key():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1", headers={"X-API-Key": INVALID_API_KEY})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}

@pytest.mark.asyncio
async def test_read_item_not_found():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/999", headers={"X-API-Key": VALID_API_KEY})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

@pytest.mark.asyncio
async def test_create_item_validation_error():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items/", json={"name": "New Item", "price": "invalid_price"}, headers={"X-API-Key": VALID_API_KEY})
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_cause_error_returns_500():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cause_error", headers={"X-API-Key": VALID_API_KEY})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
