# This file answers a very popular question:
# "How can I connect frontend and backend?" - asked the shitty coder

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def root():
    return FileResponse("public/index2.html")


@app.post("/hello")
# def hello(name = Body()):
@app.post("/hello")
def hello(
    name: str = Body(embed=True, min_length=3, max_length=20),
    age: int = Body(embed=True, ge=18, lt=111)
):
    return {"message": f"{name}, your age - {age}"}