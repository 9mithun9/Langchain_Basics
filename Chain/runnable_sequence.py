from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnableSequence, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o"
)

class Player(BaseModel):
    name: str
    country: str 

pyd_parser = PydanticOutputParser(pydantic_object=Player)

prompt_01 = PromptTemplate(
    input_variables=['topic'],
    template="Generate a famous player name and his country from the sport: {topic} \n {format_instructions}",
    partial_variables={
        "format_instructions" : pyd_parser.get_format_instructions()
    }
)

extract_fields = RunnableLambda(lambda x: {
    "name": x.name,
    "country": x.country
})

prompt_2 = PromptTemplate(
    input_variables=['name', 'country'],
    template="Write me a joke about the player {name} the {country}'s capital"
)

parser = StrOutputParser()

#chain = prompt_01 | model | pyd_parser | extract_fields | prompt_2 | model | parser

chain = RunnableSequence(prompt_01, model, pyd_parser, extract_fields, prompt_2, model, parser )

result = chain.invoke({'topic': 'Polo'})
print(result)



