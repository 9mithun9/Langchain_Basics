from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.schema.runnable import RunnableSequence, RunnableParallel, RunnableLambda
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

model_01 = ChatOpenAI(
    model = "gpt-4o"
)

model_02 = ChatOpenAI(
    model = "gpt-3.5-turbo"
)

class War(BaseModel):
    period: str
    countries: str
    total_loss: str

pyd_parser = PydanticOutputParser(pydantic_object=War)
str_parser = StrOutputParser()

prompt_summary = PromptTemplate(
    input_variables=['topic'],
    template="Write me a 3 line summary of the '{topic}' war"
)

prompt_table = PromptTemplate(
    input_variables=['topic'],
    template="Give me the period, countries, total loss in USD in the '{topic}' war in the follwing format \n {format_instructions}",
    partial_variables={
        "format_instructions": pyd_parser.get_format_instructions()
    }
)


parallel_chain = RunnableParallel({
    'summary': RunnableSequence(prompt_summary, model_01, str_parser),
    'table': prompt_table | model_02 | pyd_parser
})

#topic = input('Which War you want to know about? : ')
#result = parallel_chain.invoke({'topic': topic})
#print(result)

prompt_quiz = PromptTemplate(
    input_variables=['summary', 'table'],
    template="Create 5 Quiz from {summary} and {table}"
)

#chain = parallel_chain | prompt_quiz | model_01 | str_parser 
#topic = input('Which War you want to know about? : ')
#result_01 = chain.invoke({'topic': topic})
#print(result_01)

parallel_chain_02 = RunnableParallel({
    'summary': RunnableLambda(lambda x: x['summary_input']) | prompt_summary | model_01 | str_parser,
    'table': RunnableLambda(lambda x: x['table_input']) | prompt_table | model_02 | pyd_parser
})

chain = parallel_chain_02 | prompt_quiz | model_01 | str_parser 

result_02 = chain.invoke({
    'summary_input' : 'Israel-Iran',
    'table_input': 'Azerbaizan-Armenia'
})

print(result_02)
chain.get_graph().print_ascii()



