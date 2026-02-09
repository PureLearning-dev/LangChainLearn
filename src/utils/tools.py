import datetime
from langchain_core.tools import tool

from src.utils.models import deep_seek_v3_model


@tool
def get_date_time():
    """获取当前日期"""
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    llm = deep_seek_v3_model()
    # 将工具绑定到大模型上
    llm_with_tools = llm.bind_tools([get_date_time])
    query = "现在几点了？请调用工具获取准确时间。"
    response = llm_with_tools.invoke(query)

    if response.tool_calls:
        print("AI 正在申请调用工具...")

        # 3. 手动执行工具（在 LangGraph 或 AgentExecutor 中这一步是自动的）
        tool_call = response.tool_calls[0]
        selected_tool = {"get_date_time": get_date_time}[tool_call["name"]]
        tool_output = selected_tool.invoke(tool_call["args"])

        # 4. 将工具结果回传给 AI
        # 注意：这里需要把原始消息、工具请求消息、工具结果消息全部发给 AI
        from langchain_core.messages import HumanMessage, ToolMessage

        final_response = llm_with_tools.invoke([
            HumanMessage(content=query),
            response,  # AI 的第一次回复（包含 tool_call ID）
            ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"])
        ])

        print(f"最终 AI 回复: {final_response.content}")
    else:
        # 如果 AI 没调工具直接回答了（通常会答错）
        print(f"AI 直接回答: {response.content}")