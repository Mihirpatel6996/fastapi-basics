# FastAPI Learning Notes

## My Learning Resources
- [My Personal FastAPI Notes (Google Doc)](https://docs.google.com/document/d/1Y6dOtwnon3vZTXHdOyq2nT6Wi5RLZUlan1OaV7o0zaA/edit?usp=sharing)

## Setup and Installation
```bash
pip install fastapi uvicorn
```

Run the server:
```bash
uvicorn main:app --reload
# main = file name
# app = FastAPI instance
# --reload = auto-reload on changes
```

## Basic Concepts

### 1. Path Operations
- Uses HTTP methods (GET, POST, etc.)
- Defined using decorators: `@app.get()`, `@app.post()`
- Basic structure:
```python
@app.get("/")
def root():
    return {"message": "Hello World"}
```

### 2. Path Parameters
Three main types of parameters in FastAPI:
1. Path Parameters
2. Query Parameters
3. Request Body

#### Path Parameters
```python
@app.get("/blog/{id}")
def show_blog(id: int):
    return {"blog_id": id}
```
- Part of the path
- Enclosed in curly braces
- Can be type-hinted (int, str, etc.)
- Example URL: `/blog/123`

Important: Static routes must come before dynamic routes
```python
@app.get("/blog/unpublished")  # ✅ Correct order
@app.get("/blog/{id}")         # Dynamic route after static
```

### 3. Query Parameters
Query parameters are passed after `?` in URL

#### Basic Query Parameter
```python
@app.get("/blog")
def show_limit(limit):
    return {'data': f'{limit} blogs fetched'}
```
URL: `/blog?limit=10`

#### Multiple Query Parameters
```python
@app.get("/blog")
def show_limit(limit, published: bool):
    return {'data': f'{limit} {"published" if published else ""} blogs'}
```
URL: `/blog?limit=10&published=true`

#### Optional Query Parameters
```python
from typing import Optional

@app.get("/blog")
def show_limit(limit=10, published: bool = True, sort: Optional[str] = None):
    return {'data': f'{limit} blogs'}
```
URL: `/blog` (uses defaults)
URL: `/blog?limit=20&published=false&sort=date`

### 4. Request Body
Using Pydantic models for request validation:

```python
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f"Blog created with title {request.title}"}
```

## API Documentation
FastAPI automatically generates API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Response Examples

### Path Parameter Response
```
GET /blog/28
Response: {"data": 28}
```

### Query Parameter Response
```
GET /blog?limit=10&published=true
Response: {"data": "10 published blogs data fetched"}
```

### Error Response Example
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "id"],
      "msg": "Input should be a valid integer",
      "input": "invalid"
    }
  ]
}
```


[Previous content remains the same...]

## Additional Advanced Concepts

### 5. Response Models
```python
from pydantic import BaseModel
from typing import List

class BlogResponse(BaseModel):
    title: str
    likes: int

@app.get("/blog/{id}", response_model=BlogResponse)
def get_blog(id: int):
    return {"title": "My Blog", "likes": 100, "secret_data": "hidden"}
```
Response models help filter out unwanted data and validate responses.

### 6. Status Codes
```python
from fastapi import status

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    return blog
```

Common Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

### 7. Dependencies
```python
from fastapi import Depends

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/blogs")
def get_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).all()
```

### 8. Background Tasks
```python
from fastapi import BackgroundTasks

def notify_subscribers(email: str):
    # Send email notification
    pass

@app.post("/blog")
def create_blog(blog: Blog, background_tasks: BackgroundTasks):
    background_tasks.add_task(notify_subscribers, "user@example.com")
    return {"message": "Blog created"}
```

### 9. CORS (Cross-Origin Resource Sharing)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 10. File Handling
```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

### 11. Error Handling
```python
from fastapi import HTTPException

@app.get("/blog/{id}")
def get_blog(id: int):
    if id > 100:
        raise HTTPException(
            status_code=404,
            detail="Blog not found",
            headers={"X-Error": "Blog ID too high"},
        )
    return {"blog_id": id}
```

### 12. Authentication
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Project Structure Best Practices
```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── blogs.py
│   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── blog.py
│   └── schemas/
│       ├── __init__.py
│       └── blog.py
├── tests/
│   ├── __init__.py
│   └── test_blogs.py
├── requirements.txt
└── README.md
```

## Testing
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

## Deployment Considerations
1. Use ASGI servers in production:
   - Uvicorn
   - Gunicorn with Uvicorn workers
2. Environment variables for configuration
3. Docker containerization
4. Load balancing
5. Security headers
6. Rate limiting

## Performance Tips
1. Use async functions for I/O-bound operations
2. Implement caching where appropriate
3. Use connection pooling for databases
4. Optimize database queries
5. Use background tasks for heavy operations

## Useful FastAPI Extensions
- FastAPI Users: User management
- FastAPI SQLAlchemy: Database integration
- FastAPI Cache: Caching support
- FastAPI JWT Auth: JWT authentication
- FastAPI Admin: Admin interface

## Best Practices
1. Always place static routes before dynamic routes
2. Use type hints for better validation
3. Use Pydantic models for request body validation
4. Set default values for optional parameters
5. Use proper HTTP methods for operations:
   - GET: Fetch data
   - POST: Create new data
   - PUT: Update data
   - DELETE: Remove data

## Additional Resources
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
