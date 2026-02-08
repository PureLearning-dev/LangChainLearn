import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def verify_environment():
    print(f"--- 环境信息 ---")
    print(f"Python 路径: {sys.executable}")
    print(f"Python 版本: {sys.version}")

    try:
        # 1. 验证基础组件导入
        prompt = ChatPromptTemplate.from_template("你好，我是{name}")
        # 2. 验证模型组件导入 (此处仅初始化对象，不联网)
        model = ChatOpenAI(model="gpt-3.5-turbo", api_key="sk-test-only")

        # 3. 验证典型的 LCEL 链式组合 (这是 LangChain 的精髓)
        chain = prompt | model

        print(f"\n✅ 基础组件验证成功!")
        print(f"✅ 链式对象构建成功: {type(chain)}")

    except Exception as e:
        print(f"\n❌ 验证失败: {e}")


if __name__ == "__main__":
    verify_environment()