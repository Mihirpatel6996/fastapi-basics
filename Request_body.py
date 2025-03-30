from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional



app = FastAPI()

@app.get("/")
def root():
    return {"message": "learning about Requests"}


class Blog(BaseModel):
    title:str
    body:str
    publised: Optional[bool]

    

@app.post('/blog')
def create_blog(request:Blog):
    return {'data' : f"Blog created with title {request.title}"}

'''http://127.0.0.1:8000/docs#/default/create_blog_blog_post

output : 
{
  "data": "Blog created with title Metamorphosis"
}
'''


