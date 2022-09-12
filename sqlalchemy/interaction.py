# Creating a db session

from sqlalchemy.orm import sessionmaker
from alchemy_db import engine, Person

SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()


# Here is the simplest CRUD implementation (Create, Read, Update, Delete)
# Let's create a Person object to add in db
tom = Person(name="Tom", age=38)
db.add(tom)     # Adding to db
db.commit()     # Saving changes
db.refresh(tom)  # Update object state

# We use refresh() when we are going to use this object further

print(tom.id)  # You can get object id

# You can add even more objects!
bob = Person(name="Bob", age=42)
sam = Person(name="Sam", age=25)

# Alternatively, you can add many objects with db.add_all[bob, sam])
db.add(bob)
db.add(sam)
db.commit()

# This is how we can get data from the database
# Getting all objects
people = db.query(Person).all()
for p in people:
    print(f"{p.id}.{p.name} ({p.age})")

# Getting one object by id
first_person = db.get(Person, 1)
print(f"{first_person.name} - {first_person.age}")
# Tom - 38

# We can also filter our queries
people = db.query(Person).filter(Person.age > 30).all()
for p in people:
    print(f"{p.id}.{p.name} ({p.age})")

# This is how you can get only one object
first = db.query(Person).filter(Person.id == 1).first()
print(f"{first.name} ({first.age})")

# get() and first() usually return None if object is not found,
# so you are to create an if statement to check that

# You can also change the values right away
# Change the values
tom.name = "Tomas"
tom.age = 22

db.commit()  # Save changes

# You can also delete objects from the database
bob = db.query(Person).filter(Person.id == 2).first()
db.delete(bob)  # Delete object
db.commit()     # Save changes
