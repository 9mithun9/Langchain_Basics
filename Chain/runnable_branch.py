from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.schema.runnable import RunnableSequence, RunnableLambda, RunnableBranch, RunnableParallel, RunnablePassthrough
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o"
)

prompt_email = PromptTemplate(
    template = "Generate an email either a general Query or refund related or complain related"
)

class Email(BaseModel):
    sentiment: Literal["General", "Refund", "Complain"] = Field(description="Sentiment of the analysis should be either 'General' or 'Refund' or 'Query'")

pyd_parser = PydanticOutputParser(pydantic_object=Email)
str_parser = StrOutputParser()

prompt_ananlysis = PromptTemplate(
    input_variables=['email'],
    template="Analyze the sentiment of the {email} either into one category- General, Refund or Complain following the pattern below: \n {format_instructions}",
    partial_variables={
        "format_instructions": pyd_parser.get_format_instructions()
    }
)

email_chain = prompt_email | model | str_parser

parallel_chain = RunnableParallel({
    'email': RunnablePassthrough(),
    'sentiment': prompt_ananlysis | model | pyd_parser

})

#print((email_chain | parallel_chain).invoke({}))

prompt_general = PromptTemplate(
    input_variables=['email','sentiment'],
    template="Generate a 3 line response of this {email} based on the sentiment: {sentiment}"
)
prompt_refund = PromptTemplate(
    input_variables=['email','sentiment'],
    template="Generate a 3 line response email of this {email} based on the sentiment: {sentiment}. This reply email should have sufficient info regarding the refund related issue"
)
prompt_complain = PromptTemplate(
    input_variables=['email','sentiment'],
    template="Reply query of this {email} based on the sentiment: {sentiment}. This reply email should suffice the customer's query"
)



branch_chain = RunnableBranch(
    (lambda x: x['sentiment'].sentiment == "General", prompt_general | model | str_parser),
    (lambda x: x['sentiment'].sentiment == "Refund", prompt_refund | model | str_parser),
    (lambda x: x['sentiment'].sentiment == "Complain", prompt_complain | model | str_parser),
    RunnableLambda(lambda x: "No response for the sentiment")
)

chain = email_chain | parallel_chain | branch_chain
result = chain.invoke({})
print(result)
chain.get_graph().print_ascii()

