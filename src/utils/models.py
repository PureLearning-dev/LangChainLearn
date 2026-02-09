import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def deep_seek_v3_model():
    return ChatOpenAI(
        model="deepseek-chat",  # DeepSeek V3 的官方调用名称
        temperature=0.5,  # 设置 0.5 兼顾创造力和稳定性
        base_url="https://api.deepseek.com",  # 官方 API 地址
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

def deep_seek_v3_query(message):
    # 初始化模型
    llm = ChatOpenAI(
        model="deepseek-chat",  # DeepSeek V3 的官方调用名称
        temperature=0.5,  # 设置 0.5 兼顾创造力和稳定性
        base_url="https://api.deepseek.com",  # 官方 API 地址
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    # 执行调用并返回结果
    # 这里直接调用 invoke 会返回一个 AIMessage 对象
    response = llm.invoke(message)
    print(response.content)

def deep_seek_v3_query_stream(message):
    llm = ChatOpenAI(
        model="deepseek-chat",  # DeepSeek V3 的官方调用名称
        temperature=0.5,  # 设置 0.5 兼顾创造力和稳定性
        base_url="https://api.deepseek.com",  # 官方 API 地址
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )
    response = llm.stream(message)

    for chunk in response:
        print(chunk.content, end="", flush=True)

if __name__ == "__main__":
    query = input("请输入问题:")
    deep_seek_v3_query_stream(query)
