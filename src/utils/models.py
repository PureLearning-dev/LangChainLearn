from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser

def deep_seek_v3_stream(message):
    """
    使用 V3 模型进行流式对话
    """
    # 实例化 V3 模型
    # model="deepseek-chat" 指向的就是最新的 V3
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.7,  # 0.7 适合创意和日常对话
        streaming=True,  # 开启流式支持
        max_retries=2,  # 失败自动重试
    )

    # 开始流式输出
    for chunk in llm.stream(message):
        print(chunk.content, end="", flush=True)

def deep_seek_pro_stream(message):
    """
    专门针对付费模型 (deepseek-reasoner/R1) 的流式输出函数
    """
    # 初始化付费模型
    # model="deepseek-reasoner" 对应最新的 R1 模型
    llm = ChatDeepSeek(
        model="deepseek-reasoner",
        max_retries=3
    )

    print("🚀 [付费版 R1] 正在深度思考中...\n")

    # 在 R1 中，我们需要区分“推理”和“最终答案”
    # 注意：并非所有版本的 LangChain 都能直接解析推理字段
    # 如果是标准的 ChatDeepSeek 库，我们可以这样捕获：

    for chunk in llm.stream(message):
        # 1. 尝试捕获推理内容 (Reasoning Content)
        # DeepSeek 专用库通常将推理内容放在 additional_kwargs 中
        if hasattr(chunk, 'additional_kwargs') and 'reasoning_content' in chunk.additional_kwargs:
            # 灰度显示推理过程（模拟思考感）
            reasoning = chunk.additional_kwargs['reasoning_content']
            print(f"\033[90m{reasoning}\033[0m", end="", flush=True)

        # 2. 正常打印最终答案内容
        if chunk.content:
            print(chunk.content, end="", flush=True)

# src/models.py

def deep_seek_v3_chain():
    """
    创建一个专用的 V3 链条实例
    """
    llm = ChatDeepSeek(model="deepseek-chat", temperature=0.7)
    # 返回一个未填充数据的链条
    # 加上 StrOutputParser() 可以直接把结果转为字符串，方便流式输出
    return llm | StrOutputParser()