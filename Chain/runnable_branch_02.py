from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableSequence, RunnablePassthrough, RunnableBranch, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model = "gpt-4o"
)

str_parser = StrOutputParser()

prompt_topic = PromptTemplate(
    input_variables=['topic'],
    template="Generate a detailed report on this {topic} topic"
)

prompt_500 = PromptTemplate(
    input_variables=['text'],
    template="Keep the total number of words of the following report below 500. \n {text}"
)

branch_chain = RunnableBranch(
    (lambda x: len(x.split()) > 500, prompt_500 | model | str_parser),
    RunnablePassthrough()
)

chain = prompt_topic | model | str_parser | branch_chain
result = chain.invoke({'topic':'Gulf War 1990'})
print(result)
chain.get_graph().print_ascii()