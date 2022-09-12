# This file answers a very popular question:
# "How can I connect frontend and backend?" - asked the shitty coder

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field


app = FastAPI()

# This is the first way you can get the data from a client

# @app.get("/")
# def root():
#     return FileResponse("public/index2.html")
#
#
# @app.post("/hello")
# # def hello(name = Body()):
# @app.post("/hello")
# def hello(
#     name: str = Body(embed=True, min_length=3, max_length=20),
#     age: int = Body(embed=True, ge=18, lt=111)
# ):
#     return {"message": f"{name}, your age - {age}"}

# But you can also use pydantic models to do the same thing


# You can make the age optional by Union[int, None] = None
# Detailed attribute settings using the Field class
class Person(BaseModel):
    name: str = Field(default='Undefined', min_length=3, max_length=20)
    age: int = Field(default=18, ge=18, lt=111)


# Returning the root
@app.get("/")
def root():
    return FileResponse("public/index2.html")


# Returning the attributes of Person object
@app.post("/hello")
def hello(person: Person):
    return {"message": f"Hello, {person.name}, your age - {person.age}"}

# Similarly, you can get a list of model objects but you are to change JS response a little bit
# const response = await fetch("/hello", {
#     method: "POST",
#     headers: { "Accept": "application/json", "Content-Type": "application/json" },
#     body: JSON.stringify([
#         { name: "Tom", age: 38 },
#         { name: "Bob", age: 41 },
#         { name: "Sam", age: 25 }
#     ])
# });
# const data = await response.json();
# console.log(data);
#
# @app.post("/hello")
# def hello(people: list[Person]):
#     return {"message": people}
#
# Or we can get lists out of JS
#
# const response = await fetch("/hello", {
#     method: "POST",
#     headers: { "Accept": "application/json", "Content-Type": "application/json" },
#     body: JSON.stringify({
#         name: "Tom",
#         languages: ["Python", "JavaScript"]
#     })
# });
# const data = await response.json();
# console.log(data);      // {message: "Name: Tom. Languages: ['Python', 'JavaScript']"}
#
# @app.post("/hello")
# def hello(person: Person):
#     return {"message": f"Name: {person.name}. Languages: {person.languages}"}
#
# You can also set the attribute to a default value in case the request does not contain the corresponding data:
# class Person(BaseModel):
#     name: str
#     languages: list = ["Java", "Python", "JavaScript"]


# We can also have one more pydantic scheme if Person works in some Company
class Company(BaseModel):
    name: str

# For simplicity, here the company class has only one attribute - the name of the company.
# Sending a request in javascript code in this case could look like this:

# const response = await fetch("/hello", {
#     method: "POST",
#     headers: { "Accept": "application/json", "Content-Type": "application/json" },
#         body: JSON.stringify({
#         name: "Tom",
#         company: {name: "Google"}
#     })
# });
# const data = await response.json();
# console.log(data);