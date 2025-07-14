from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class Employee(BaseModel):
    name: str
    age: int = Field(ge=18, le=65, description="Age of the employee must be between 18 and 65")
    department: str
    salary: Optional[float]=None 
    email: EmailStr

emp_01 = {
    "name": "Jane Smith",
    "age": 30,
    "department": "Marketing",
    #"salary": 60000.0,
    "email": "dhdh@gmail.com"
}

employee_01 = Employee(**emp_01)

print(dict(employee_01))

