# this code is all about fastapi installation and path parameters



# pip install uvicorn, fastapi

# run - uvicorn main:app --reload
# main is the name of the file 
# app is the instance created in the code 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")

# here get is the operation we have (get and post )
# and ("/") is the path we can have ( /about , /home, / contact us)
def root():
    return {"message": "Hello World"}  # displays this {"message":"Hello World"} in web

#and the function associated is called as path operation function
# @app and this is called path operator decorator 



# path parameters 

# concept-3 
'''it is always recommended to add static paths above dynamic path in this case "/blog/unpublished" is static
and blig/{id} is dynamic and fastapi will read it line by line so if we had this path => "/blog/unpublished" below the dynamic path "blog/{id}" that will never run because th app will assume that "/blog/unpublished" is part of blog/{id}
'''
@app.get("/blog/unpublished")

def show_unpublished ():
    return {'data' : "unpublised data"}

'''{"data":"unpublised data"}'''




# concept -1

@app.get ("/blog/{id}")

def show_blog_with_id(id:int):   # 2. if we provide int here data will print like this {"data" : 28}
    return {'data' : id }


'''
 1. for any link  ex http://127.0.0.1:8000/blog/28 it displays {"data":"28"}  on web 
'''

'''
3. def show_blog_with_id(id:int):  when we are giving like this if suppose if we pass a string to route insted of route it will return this 

http://127.0.0.1:8000/blog/"hey this is mihir"

{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "\"hey this is mihir\""
    }
  ]
}

'''

# concept -2 

@app.get ("/{id}/comments")
def show_comments(id):
    return {'data' : f"this is the comments for id {id}"}

'''
for any link ex http://127.0.0.1:8000/30/comments it displays {{"data":"this is the comments for id 30"}} in the web 
'''


