from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(
    model="gpt-3.5-turbo")

temp1 = PromptTemplate(
    input_variables=["topic"],
    template="Write a detailed report about {topic}"
)

prompt1 = temp1.invoke({'topic': 'Agentic AI'})
result1 = model.invoke(prompt1)

temp2 = PromptTemplate(
    input_variables=["text"], 
    template="Write 5 lines summary of these: {text}"
)
promt2 = temp2.invoke({'text': result1.content})
result2 = model.invoke(promt2)

print("Detailed Report:")
print(result1.content)
print("\nSummary:")
print(result2.content)