# In this file, I am going to show you how to submit forms using HTML and Python

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

app = FastAPI()

# Donwloading setting our response file
@app.get("/")
def root():
    return FileResponse("public/forms.html")


# Create a server response (filtering the data with Form())
@app.post("/postdata")
def postdata(
    username: str = Form(default="Undefined", min_length=2, max_length=20),
    userage: int = Form(default=18, ge=18, lt=111), languages: list = Form()
):
    return {"name": username, "age": userage, "languages": languages}

