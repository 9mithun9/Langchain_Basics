from langchain_core.tools import tool

def factorial(a):

    """Genrate factorial of a number"""
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact 



def factorial(a: int) -> int:

    """Genrate factorial of a number"""
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact 


@tool
def factorial(a: int) -> int:

    """Genrate factorial of a number"""
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact 


result = factorial.invoke({'a':5})
print(result)
print(factorial.name)
print(factorial.description)
print(factorial.args)