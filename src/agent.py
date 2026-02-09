import os
from dataclasses import dataclass
from dotenv import load_dotenv

# 核心库导入
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy

# 1. 定义中文系统提示词
SYSTEM_PROMPT = """你是一位气象预报专家，说话风格非常幽默，喜欢用谐音梗。

你有权访问以下两个工具：
- get_weather_for_location: 用于获取特定城市的实时天气。
- get_user_location: 用于获取当前用户的所在地。

如果用户询问天气，请务必确认地点。如果从问题中可以看出他们是指“所在地”，请先使用 get_user_location 工具找到他们的位置。"""

# 2. 定义上下文架构（Context）
@dataclass
class Context:
    """自定义运行时上下文模式。"""
    user_id: str

# 3. 定义中文工具
@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    # 模拟返回：总是晴天
    return f"{city}的天气总是晴空万里！"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 检索用户信息（所在地）。"""
    user_id = runtime.context.user_id
    # 模拟逻辑：ID为1在上海，其他在深圳
    return "上海" if user_id == "1" else "深圳"

# 4. 初始化模型 (DeepSeek)
load_dotenv()

model = init_chat_model(
    model="deepseek-chat",
    model_provider="openai",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.7,
    timeout=10,
    max_tokens=1000
)

# 5. 定义结构化输出格式
@dataclass
class ResponseFormat:
    """Agent 的响应架构。"""
    # 幽默的回答（必填）
    punny_response: str
    # 天气情况的简要描述（选填）
    weather_conditions: str | None = None

# 6. 设置记忆与 Agent
checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# 7. 运行 Agent
# thread_id 用于区分不同的会话 ID
config = {"configurable": {"thread_id": "888"}}

# 第一次对话：询问天气
print("--- 第一次对话 ---")
response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面天气怎么样？"}]},
    config=config,
    context=Context(user_id="1")
)

# 打印结构化结果
structured = response['structured_response']
print(f"谐音梗回复: {structured.punny_response}")
print(f"具体天气: {structured.weather_conditions}")

# 第二次对话：继续之前的上下文
print("\n--- 第二次对话 ---")
response = agent.invoke(
    {"messages": [{"role": "user", "content": "太棒了，谢谢你！"}]},
    config=config,
    context=Context(user_id="1")
)

print(f"谐音梗回复: {response['structured_response'].punny_response}")