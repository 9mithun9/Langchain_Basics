from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableParallel 


load_dotenv()

model_1 = ChatOpenAI(
    model="gpt-4o"
)
model_2 = ChatOpenAI(
    model="gpt-3.5-turbo"
)

prompt_detail = PromptTemplate(
    input_variables=["topic"],
    template="Write a detailed report about {topic}"
)

prompt_summary = PromptTemplate(
    input_variables=["text"],
    template="Write 5 lines summary of these: {text}"
)

prompt_QA = PromptTemplate(
    input_variables=["text"],  
    template="Generate 5 Quizz from this: {text}"
)

prompt_merge = PromptTemplate(
    input_variables=["summary", "quiz"],
    template="Merge these: {summary} and {quiz} into a single coherent text, ensuring that the quiz questions are relevant to the summary provided."
)

parser = StrOutputParser()
parallel_chain = RunnableParallel(
    { 
        "summary": prompt_detail | model_1 | parser | prompt_summary | model_2 | parser, 
        "quiz": prompt_detail | model_1 | parser | prompt_QA | model_2 | parser
    }
)

chain = parallel_chain | prompt_merge | model_1 | parser
result = chain.invoke({'topic': 'Transformer: Attention is All You Need'})
print(result)
chain.get_graph().print_ascii()






