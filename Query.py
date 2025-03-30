from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Query Parameters"}


# Query  parameters 



@app.get("/blog/unpublished")

def show_unpublished ():
    return {'data' : "unpublised data"}





# concept -1

@app.get ("/blog")

def show_limit(limit):
    return {'data' : f'{limit} blogs data fetched'}

'''
http://127.0.0.1:8000/blog?limit=10
output : -{"data":"10 blogs data fetched"}

'''


# concept -2 
@app.get ("/show_blog")

def show_limit(limit,published : bool):
    if published:
        return {'data' : f'{limit} published blogs data fetched'}
    else:
        return {'data' : f'{limit}  blogs data fetched'}


'''
http://127.0.0.1:8000/show_blog?limit=10&published=true
output ==> {"data":"10 published blogs data fetched"}

http://127.0.0.1:8000/show_blog?limit=10&published=false
output ==> {"data":"10  blogs data fetched"}

http://127.0.0.1:8000/show_blog?limit=10
output ==> {"detail":[{"type":"missing","loc":["query","published"],"msg":"Field required","input":null}]}
'''



# concept - 3

from typing import Optional

@app.get ("/show_blog_DL")

def show_default_limit(limit=10 ,published : bool = True, sort : Optional[str]= None ):
    if published:
        return {'data' : f'{limit} published blogs data fetched'}
    else:
        return {'data' : f'{limit}  blogs data fetched'}


# http://127.0.0.1:8000/show_blog_DL  => {"data":"10 published blogs data fetched"}


# concept 4

@app.get ("/{id}/comments")
def show_comments(id, limit=10):
    return {'data' : f"showing {limit} comments for id {id} "}

# http://127.0.0.1:8000/29/comments => {"data":"showing 10 comments for id 29 "}
