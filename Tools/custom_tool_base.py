from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class Factorial(BaseModel):
    a: int = Field(required=True, description="The number we want to calculate the factorial of")

class FactorialTool(BaseTool):
    name: str = "Factorial",
    description: str = "Calculate the factorial of a number",
    args_schema: Type[BaseModel] = Factorial

    def _run(self, a: int) -> int:
        fact = 1
        for i in range(1,a+1):
            fact = fact * i
        return fact 

fact_tool = FactorialTool()

result = fact_tool.invoke({'a':7})
print(result)
