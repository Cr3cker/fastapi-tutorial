# WARNING! READ CAREFULLY BEFORE FOLLOWING THIS TUTORIAL!
# Do NOT listen to my advices about FastAPI! It can be DANGEROUS for your mental health and for
# your code as well. I am just a SHITTY coder who produces a lot of chaotic code and does NOT want
# to process its refactoring of any type.


from fastapi import FastAPI, Response, Path, Query, status, Header, Cookie
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Union
from datetime import datetime

app = FastAPI()

file = "public/index.html"


# Responses in FastAPI
@app.get("/")
def read_root():
    html_content = "<h2>Hello MYSITE.COM!</h2>"
    return HTMLResponse(content=html_content)


# Simple json response
@app.get("/about")
def about():
    data = {"message": "About this site"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)


@app.get("/metanit")
def metanit():
    data = "Hello MYSITE.COM!"
    # You can also use PlainTextResponse
    return Response(content=data, media_type="text/plain")


# Or you can use even more simple version of the same response
@app.get("/media", response_class=PlainTextResponse)
def media():
    return "Hello METANIT.COM"


# This is a simple example of FileResponse usage
@app.get("/file", response_class=FileResponse)
def file_html():
    return FileResponse(file)


# Or use just an alternative method
@app.get("/file_alt", response_class=FileResponse)
def root_html():
    return "public/index.html"


# This is how we can download files
@app.get("/filedownload")
def download():
    return FileResponse(file, filename="simple_html.html", media_type="application/octet-stream")


# This is an example of path parameters
@app.get("/users/{user_id}")
def users_id(_id):
    return {"users_id": _id}


# One more example of path parameters (you can also use - to separate path parameters)
@app.get("/users/{name}/{age}")
def users_id(name, age):
    return {"name": name, "age": age}


'''
In this case, we want requests along the path "/users/admin" to be handled by the admin() function. 
And the rest of the paths according to the pattern "/users/{name}", where the second segment represents 
the name parameter, would be processed by the users() function. However, if we access the application 
with a request http://127.0.0.1:8000/users/admin, we will see that the request is handled by the users() function, 
not admin():
'''


@app.get("/users/{name}")
def users(name):
    return {"user_name": name}


@app.get("/users/admin")
def admin():
    return {"message": "Hello admin"}

# You can do something to avoid this... Just try to assign admin() before users() function


# This is how we can use TypeHints in FastAPI
@app.get("/users/{id}")
def users(_id: int):
    return {"user_id": _id}


# Path usage to validate the parameters
@app.get("/users/{name}")
def users_name(
    name: str = Path(min_length=3, max_length=20),
    age: int = Path(gt=18, lt=111)
):
    return {"name": name, "age": age}


# You can also use regex to validate the parameters
@app.get("/users/{name}")
def users_name_regex(phone: str = Path(regex="^[1-9]")):  # This is just a random regular expression
    return {"phone": phone}


# To set the default parameters we can do this
@app.get("/users/{name}")
def users_name_default(name: str = "Undefined", age: int = 18):
    return {"name": name, "age": age}


# Additionally, you can user Query() to validate the parameters (as with Path() you can use regex patterns)
@app.get("/users/{name}")
def users_name_query(
    name: str = Query(min_length=3, max_length=20, default="Bob"),
    age: Union[int, None] = Query(default=None, ge=18, lt=111)
):
    if age is None:
        return {"name": name, "age_none": age}
    else:
        return {"name": name, "age": age}


# Here I demostrate how we can pass a list of parameters to the function (or we can use typing.List instead)
@app.get("/users")
def users(people: list[str] = Query()):
    return {"people": people}


# We can combine Query() and Path() validation in one function
@app.get("/users/{name}")
def users(
    name: str = Path(min_length=3, max_length=20),
    age: int = Query(ge=18, lt=111)
):
    return {"name": name, "age": age}


# You can send custom status codes of the function
@app.get('/notfound', status_code=404)
def notfound():
    return {"not_found": "Resourse not found"}


# To make statuses usage simpler for developers, FastAPI offer status module
@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def notfound():
    return {"message": "Resource Not Found"}


# Assigning status code in response
@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def notfound():
    return JSONResponse(content={"message": "Resource Not Found"}, status_code=404)


# You can also combine these two methods
@app.get("/users/{id}", status_code=200)
def users(response: Response, _id: int = Path()):
    if _id < 1:
        response.status_code = 400
        return {"message": "Incorrect Data"}
    return {"message": f"Id = {_id}"}


# The RedirectResponse class (inherited from Response) is used for redirection in FastAPI applications
@app.get("/old")
def old():
    return RedirectResponse("/new")


@app.get("/new")
def new():
    return PlainTextResponse("New page")


# Alternative way of redirecting
@app.get("/old", response_class=RedirectResponse)
def old():
    return "/new"


# You can also redirect to an absolute address
@app.get("/old")
def old():
    return RedirectResponse("https://fastapi.tiangolo.com")


# By default, RedirectResponse sends a status code of 307 (temporary redirect).
# If this situation does not suit you, then you can set the redirect status code using the status_code parameter
@app.get("/old")
def old():
    return RedirectResponse("/new", status_code=302)


# Or this way
@app.get("/old", response_class=RedirectResponse, status_code=302)
def old():
    return "/new"


# By using this method we can easily work with static files in our application
# Constructor of StaticFiles is StaticFiles(directory=None, packages=None, html=False, check_dir=True)
app.mount("/static", StaticFiles(directory="public", html=True))


# This example shows how to send and get headers (you can see this header included in developers tools in your browser)
@app.get("/")
def root():
    data = "Hello MYSITE.COM"
    return Response(content=data, media_type="text/plain", headers={"Secret-Code": "123459"})


# Another way of doing the same thing is to use the headers attribute
@app.get("/")
def root(response: Response):
    response.headers["Secret-Code"] = "123459"
    return {"message": "Hello MYSITE.COM"}


# Getting headers (here we can use fastapi.Headers class), defining a default value for user_agent
@app.get("/")
def header(user_agent: Union[str, None] = Header()):
    return {"User-Agent": user_agent}


# This example shows hot to work with cookies on the server
@app.get("/")
def cookie(response: Response):
    now = str(datetime.now())
    response.set_cookie(key="last_visit", value=now)
    return {"message": "Cookies were set"}


# You can do the same thing using Response object
@app.get("/")
def response():
    now = str(datetime.now())
    response = JSONResponse(content={"message": "Cookies were set"})
    response.set_cookie(key="last_visit", value=now)
    return response


# To get cookies on the server you can use the following
@app.get("/")
def cookies(last_visit: Union[str, None] = Cookie(default=None)):
    if last_visit is None:
        return {"message": "This is your first visit to this site"}
    else:
        return {"message": f"Your last visit to this site {last_visit}"}


