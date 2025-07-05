from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableSequence, RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o"
)

prompt_summary = PromptTemplate(
    input_variables=['country'],
    template="Give a 1 line summary of the {country}'s capital"
)

str_parser = StrOutputParser()

chain_summary_generator = prompt_summary | model | str_parser

paraller_chain = RunnableParallel({
    'summary': RunnablePassthrough(),
    'Word_count' : RunnableLambda(lambda x: len(x.split()))
})

chain = chain_summary_generator | paraller_chain
country = input('Name a country: ')
result = chain.invoke({'country': country})
print(result)
chain.get_graph().print_ascii()

