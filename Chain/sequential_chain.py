from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o"
)

prompt1 = PromptTemplate(
    input_variables=["topic"],
    template="Write a detailed report about {topic}"
)

class Film(BaseModel):
    director: str = Field(description="Name of the movie director")
    runtime: str = Field(description="Runtime of the movie")
    box_office_collection: str = Field(description="Box office collection of the movie")
    release_date: str = Field(description="Release date of the movie")
    awards: list[str] = Field(default_factory=list, description="List of awards won by the movie")

parser = PydanticOutputParser(pydantic_object=Film)


prompt2 = PromptTemplate(
    input_variables=["text"],  
    template="Write key points based on these: {text} \n {format_instructions}",
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt1 | model | StrOutputParser() | prompt2 | model | parser

result = chain.invoke({'topic': 'Schindler\'s List'})
print(result)
chain.get_graph().print_ascii()
