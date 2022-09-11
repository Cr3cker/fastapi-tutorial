import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())


# Fake database of Person objects
people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]

# Defining the constant for the error message
ERROR_MESSAGE = "User not found"


# This will help us to find users in so-called "database"
def find_person(id):
    for person in people:
        if person.id == id:
            return person
    return None


app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index_api.html")


@app.get("/api/users")
def get_people():
    return people


@app.get("/api/users/{id}")
def get_person(id):
    # get user by id
    person = find_person(id)
    print(person)
    # if user is not found then return status code and error message
    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": ERROR_MESSAGE}
        )
    # if user is found we send him
    return person


@app.post("/api/users")
def create_person(data=Body()):
    person = Person(data["name"], data["age"])
    # add object to the list people
    people.append(person)
    return person


@app.put("/api/users")
def edit_person(data=Body()):
    # get user by id
    person = find_person(data["id"])
    # if user is not found then return status code and error message
    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": ERROR_MESSAGE}
        )
    # if user is found we change his data and return
    person.age = data["age"]
    person.name = data["name"]
    return person


@app.delete("/api/users/{id}")
def delete_person(id):
    # get user by id
    person = find_person(id)

    # if user is not found then return status code and error message
    if person is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": ERROR_MESSAGE}
        )

    # if user is found we delete him
    people.remove(person)
    return person
