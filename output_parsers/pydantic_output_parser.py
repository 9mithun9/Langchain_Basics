## Pydantic Output Parser Example
# This example demonstrates how to use PydanticOutputParser to validate the output of a language model against a Pydantic schema.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define the Pydantic model
class MovieDetails(BaseModel):
    director: str = Field(description="Name of the movie director")
    runtime: str = Field(description="Runtime of the movie")
    box_office_collection: str = Field(description="Box office collection of the movie")
    release_date: str = Field(description="Release date of the movie")
    awards: list[str] = Field(default_factory=list, description="List of awards won by the movie")

# Initialize the model
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0  # Lower temperature for more deterministic output
)

# Create the parser
parser = PydanticOutputParser(pydantic_object=MovieDetails)

# Define the prompt template
temp = PromptTemplate(
    input_variables=["movie"],
    template="""You are a movie database expert. Provide the director, runtime, box office collection, release date, and any awards won by the movie {movie}. /n {format_instructions}""", 
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }   
)

# Solution: 01
prompt = temp.invoke({'movie': 'The Mystic River'})
#print(prompt)
result = model.invoke(prompt)
result = parser.parse(result.content)
print(result)

# Solution: 02
chain = temp | model | parser
#result = chain.invoke({'movie': 'Batman begins'})
#print(result)
