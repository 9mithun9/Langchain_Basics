from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-3.5-turbo")

temp1 = PromptTemplate(
    input_variables=["topic"],
    template="Write a detailed report about {topic}"
)

temp2 = PromptTemplate(
    input_variables=["text"], 
    template="Write 5 lines summary of these: {text}"
)

parser = StrOutputParser()

chain = temp1 | model | parser | temp2 | model | parser

result = chain.invoke({'topic': 'Phetchabun GDP'})

print(result)

chain.get_graph().print_ascii()