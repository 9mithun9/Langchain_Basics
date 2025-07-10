from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class Factorial(BaseModel):
    a: int = Field(required=True, description='The number that we want to calculate the factorial of')



def factorial(a):
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact 


fact_tool = StructuredTool.from_function(
    func=factorial,
    name="Factorial",
    description="Calculate the factorial of a number",
    args_schema=Factorial
)

result = fact_tool.invoke({'a':6})

print(result)
print(fact_tool.name)
print(fact_tool.description)
print(fact_tool.args)