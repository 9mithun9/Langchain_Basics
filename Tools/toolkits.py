from langchain_core.tools import tool

@tool
def factorial(a: int) -> int:

    """Genrate factorial of a number"""
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact 

@tool
def square(a: int) -> int:

    """Genrate the square of a number"""
    return a * a


class MathToolKit:
    def get_tools(self):
        return [factorial, square]
    
math_kit = MathToolKit()
tools = math_kit.get_tools()

for tool in tools:
    result = tool.invoke({'a':7})
    print(result)