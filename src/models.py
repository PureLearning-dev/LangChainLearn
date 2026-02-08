from langchain_deepseek import ChatDeepSeek


def deep_seek_mode(message):
    llm = ChatDeepSeek(model="deepseek-chat")
    return llm.invoke(message)