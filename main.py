from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI(title="API with Key Authentication")

# API Key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In a real app, this would be stored securely
VALID_API_KEY = "your-secret-api-key"

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def not_found_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Resource not found"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Sample data
items = {
    1: {"name": "Item 1", "description": "First item", "price": 10.0},
    2: {"name": "Item 2", "description": "Second item", "price": 20.0}
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/cause_error")
def cause_error(api_key: str = Depends(get_api_key)):
    raise RuntimeError("Forced internal error")

@app.get("/items/{item_id}")
def read_item(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items/")
def create_item(item: Item, api_key: str = Depends(get_api_key)):
    new_id = max(items.keys()) + 1
    items[new_id] = item.dict()
    return {"id": new_id, **item.dict()}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, api_key: str = Depends(get_api_key)):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item.dict()
    return items[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int, api_key: str = Depends(get_api_key)):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}