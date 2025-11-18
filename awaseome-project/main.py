from fastapi import FastAPI, Query, Header, Request, Path, status
from typing import Optional, List
import json
from pydantic import BaseModel
from constants import constants
from fastapi.exceptions import HTTPException

app = FastAPI(title="Fast Api project", version="1.0.0")


@app.get("/")
async def get_print():
    return {"message": "This is not good monitor"}


@app.get("/gets/{name}")
async def get_query(name: str):
    return {"message": f"This is not {name}"}


@app.get("/gets/")
async def get_query(q: str):
    return {"message": f"This is not {q}"}


@app.get("/items/")
async def read_items(q: Optional[str] = None):
    return {"q": q}


@app.get("/items/")
async def read_new_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, title="Query thing")
):
    return {"q": q}


@app.get("/items")
async def read_items(skip: str = 0, limit: int = 10, search: Optional[str] = None):
    return {"skip": skip, "limit": limit}


@app.get("/users/{user_id}")
async def read_user(user_id: int, details: Optional[bool] = False):
    return {"user_id": user_id, details: details}


@app.get("/header/")
async def read_header(
    user_agent: Optional[str] = Header(None), x_token: Optional[str] = Header(None)
):
    return {"User-agent": user_agent, "X-token": x_token}


@app.get("/raw-body/")
async def read_body(request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    return {"raw_body": body_str}


@app.post("/json-body/")
async def read_json_body(request: Request):
    body = await request.body()
    data = json.loads(body)
    return {"received": data}


class Item(BaseModel):
    name: str
    price: str
    description: Optional[str] = None


@app.post("/item/")
async def create_item(item: Item):
    return item


@app.post("/users/{user_id}/{items}")
async def create_users(
    user_id: int = Path(..., description="This id of "),
    q: Optional[str] = Query(
        None, max_length=50, description="This will make good effect"
    ),
    x_token: Optional[str] = Header(None, description="Title"),
    item: Item = None,
    request: Request = None,
):
    raw_body = await request.body()
    return {
        "user_id": user_id,
        "query": q,
        "header_token": x_token,
        "item": item,
        "raw_body": raw_body.decode("utf-8") if raw_body else None,
    }


class Category(BaseModel):
    id: str
    name: str
    price: str
    category: str
    price: float
    stock: int
    rating: float
    published_by: str


class CategoryUpdateModal(BaseModel):
    name: str
    price: str
    category: str
    price: float
    stock: int
    rating: float


@app.get("/category", response_model=List[Category])
async def get_category():
    return constants


@app.get("/category/{id}")
async def get_by_id_category(id: str):
    abc = [item for item in constants if item["id"] == int(id)]
    if abc:
        return {"message": abc}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/category/{id}")
async def delete_by_id_category(id: str):
    abc = [item for item in constants if item["id"] == int(id)]
    if abc:
        return {"message": "Success fully deleted"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/post/category", status_code=status.HTTP_201_CREATED)
async def post_by_id_category(book_data: Category):
    abc = book_data.model_dump()
    constants.append(abc)
    return constants


@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data: CategoryUpdateModal):
    abc = [item for item in constants if item["id"] == int(book_id)]
    if abc:
        abc = book_update_data
        return abc
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
