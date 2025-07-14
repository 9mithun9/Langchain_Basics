## Structured Output Parser forces the model to return a structured response
## However, it fails to validate the response against the schema

from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o"
)

response_schemas = [
    ResponseSchema( 
        name="state",
        description="The name of the state in Thailand",
        type="string"
    ),
    ResponseSchema(
        name="property",
        description="A property or feature of the state",
        type="string"
    )]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

temp = PromptTemplate(
    input_variables=["state", "property"],
    template="What is the {property} of {state} of Thailand? Please provide a detailed response. If you don't know, say 'I don't know'.\n{format_instructions}",
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    })

raw_output = (temp | model).invoke({
    'state': 'Bangkok',
    'property': 'Sports'
})

result = parser.parse(raw_output.content)
print(result)