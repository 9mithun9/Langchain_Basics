from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv

load_dotenv()

## Tool Creation
@tool
def factorial(a: int) -> int:
    """Genrates the factorial of a given numnber 'a' """
    fact = 1
    for i in range(1,a+1):
        fact = fact * i
    return fact

@tool 
def area(length: int, width: int) -> int:
    """Calculates the area of a rectangle when length and width are given"""
    return length * width


## Tool binding
model = ChatOpenAI(
    model = "gpt-4o"
)

binded_model = model.bind_tools([factorial, area])

## Tool Calling
query = HumanMessage("What is the area of a rectangle whose length and width are 56 and 12 respectively? And what is the factorial of 11?")
messages_history = [query]

call_result = binded_model.invoke(query.content)

messages_history.append(call_result)

## Tool Execution
final_result_01 = area.invoke(call_result.tool_calls[0])
final_result_02 = factorial.invoke(call_result.tool_calls[1])

messages_history.append(final_result_01)
messages_history.append(final_result_02)
print(messages_history)



