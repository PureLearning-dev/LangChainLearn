from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following from English into {language}"),
    ("user", "{text}")
])

# 这个判断主要是为了防止在引用这个文件时，导致里面的测试代码执行，造成不必要的错误
if __name__ == "__main__":
    load_dotenv()

    prompt = prompt_template.invoke(
        {
            "language": "Chinese",
            "text": "Hello, How are you? Fuck!"
        }
    )



