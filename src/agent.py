import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

analysis = ChatPromptTemplate.from_messages([
    ("user", "我该如何回答这句话{talk}")
])

if __name__ == "__main__":
    load_dotenv()
    # 使用OpenAI的标准调用大模型
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    parser = StrOutputParser()
    # 通过LCEL语法调用执行
    chain = prompt_template | llm | parser
    chain2 = {"talk":chain} | analysis | llm | parser

    # response = chain.invoke({
    #     "text": "Hello World!",
    #     "language": "中文",
    # })
    #
    # print(response)

    response2 = chain2.invoke({
        "text": "Hello World!",
        "language": "中文",
    })

    print(response2)