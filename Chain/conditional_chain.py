# Import necessary modules and classes
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# Initialize the model
# Using gpt-4o for better performance in understanding and generating text
model = ChatOpenAI(
    model="gpt-4o"
)

# Define a Pydantic model for film review sentiment
class FilmReview(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the review either positive or negative")

# Prompt to generate an audience review for a given movie topic
prompt_review = PromptTemplate(
    input_variables=["topic"],
    template="Write an audience review of the movie: {topic}"
)

# Output parsers
parser_pydantic = PydanticOutputParser(pydantic_object=FilmReview)
parser = StrOutputParser()


# Prompt to extract sentiment from a review using the FilmReview schema
prompt_feedback = PromptTemplate(
    input_variables=["text"],   
    template="Write a sentiment either positive or negative on this review: {text} \n {format_instructions}",
    partial_variables={
        "format_instructions": parser_pydantic.get_format_instructions()
    }
)


# Chain to generate a review, extract sentiment, and parse as FilmR
feedback_chain = prompt_review | model | parser | prompt_feedback | model | parser_pydantic 

print(feedback_chain.invoke({'topic': 'The Shawshank Redemption'}))

# Prompt for positive feedback response
prompt_positive = PromptTemplate(
    input_variables=["feedback"],
    template="Generate a response for the audience based on this positive feedback: {feedback}"
)

# Prompt for negative feedback response
prompt_negative = PromptTemplate(
    input_variables=["feedback"],
    template="Generate a response for the audience based on this negative feedback: {feedback}"
)


branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive",
    prompt_positive | model | StrOutputParser()),
    (lambda x: x.sentiment == "negative",
    prompt_negative | model | StrOutputParser()),
    RunnableLambda(lambda x: "No response needed for sentiment")
)

# Run the full pipeline: generate review, extract sentiment, and respond accordingly
result = (feedback_chain | branch_chain).invoke({'topic': 'Housefull5'})
print(result)

