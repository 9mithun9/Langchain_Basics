from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

person_01 : Person = {
    "name": "Alice",
    "age": 30,
}

print(person_01)