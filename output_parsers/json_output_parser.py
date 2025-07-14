from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-3.5-turbo")

parser = JsonOutputParser()

temp = PromptTemplate(
    input_variables=["movie"],
    template="Give me the names of director, runtime, box-office collection, and release date of the movie '{movie}' If there is no movie by this name, return nothing or null\n {format_instructions}",
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# Solution: 01
prompt = temp.invoke({'movie': '(&*(^*^))'})

result = model.invoke(prompt)

result = parser.parse(result.content)

# Solution: 02
chain = temp | model | parser
result = chain.invoke({'movie': 'The Good, the Bad and the Ugly'})
print(result)
