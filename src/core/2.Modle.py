import datetime
import os
from tkinter.constants import MOVETO
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

load_dotenv(verbose=True)

# 使用封装好的ChatDeepSeek模型进行快速启用
deep_seek_v3_model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
    max_tokens=2048,
    timeout=60,
)

# LangChain提供一种适用性极强的方法用于创建模型实例
deep_seek_v3_model_init = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
    max_tokens=2048,
    timeout=60,
)


from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

# 使用@tool声明一个工具（函数）供大模型调用
@tool
def get_weather(location: str) -> str:
    """获取城市的当前天气情况."""
    return f"{location}的天气十分晴朗！"

@tool
def get_date_time() -> str:
    """获取当前的时间"""
    return str(datetime.datetime.now())

if __name__ == "__main__":
    # **大模型调用**，response = deep_seek_v3_model.invoke(conversation)
    # 返回一个AIMessage类型，invoke方法需要模型将内容生成完才进行返回
    # print("response的类型:" + str(type(response)))
    # 都可以拿到内容
    # print("response text:" + response.text)
    # print("response content" + response.content)
    # 拿到一个流式对象generator，不断从这个对象获取数据
    # response_stream = deep_seek_v3_model_init.stream("Why do parrots have colorful feathers?")
    # print("response_stream的类型:" + str(type(response_stream)))
    # 返回多个AIMessageChunk对象
    # full = None  # None | AIMessageChunk
    # for chunk in response_stream:
    #     full = chunk if full is None else full + chunk
    #     print(full.text)
    # full = ""
    # for chunk in response_stream:
    #     full += chunk.text
    #     print(chunk.content, end='', flush=True)
    # print("\n")
    # # 将流式输出的内容进行拼接，可以用于上下文信息和存储
    # print("等到的完整回答为:" + full)

    # **批次处理**，同时处理三个问题。返回最终输出，如果要完成一个问题返回一个答案，需要使用batch_as_completed()
    # responses = deep_seek_v3_model_init.batch([
    #     "Why do parrots have colorful feathers?",
    #     "How do airplanes fly?",
    #     "What is quantum computing?"
    # ])
    # for response in responses:
    #     print(response.content)
    # 输出顺序会有混乱，但是存在索引号，需要根据问题以及结果重新匹配
    # for response in deep_seek_v3_model_init.batch_as_completed([
    #     "Why do parrots have colorful feathers?",
    #     "How do airplanes fly?",
    #     "What is quantum computing?"
    # ]):
    #     print(response)
    # 为了控制使用batch时的参数，可以配置batch提供的配置属性。比如控制最大并行调用数量。
    # list_of_inputs = [
    #     "Why do parrots have colorful feathers?",
    #     "How do airplanes fly?",
    #     "What is quantum computing?"
    # ]
    # 配置项是一个RunnableConfig对象，里面还存在更多的参数配置
    # config = RunnableConfig(max_concurrency=5)
    # deep_seek_v3_model_init.batch(
    #     inputs = list_of_inputs,
    #     config = config,
    # )

    # **函数调用（工具调用）**：可以让大模型具有更强大的功能，包括但不限于访问api、查看数据库、修改本地文件
    # 使用大模型的 bind_tools 进行绑定工具，后续大模型就可以根据需要进行调用了
    # 将工具绑定到大模型上，并返回一个新的带有工具的大模型实例，后续使用返回的大模型实例进行调用则可
    # model_with_tools = deep_seek_v3_model_init.bind_tools(
    #     [
    #         get_weather,
    #         get_date_time,
    #     ]
    # )
    # 这个response中会存在需要调用的函数
    # response = model_with_tools.invoke("成都今天的天气如何？")
    # for tool_call in response.tool_calls:
    #     print(f"Tool: {tool_call['name']}")
    #     print(f"Args: {tool_call['args']}")

    # **工具执行循环**：调用返回的函数，并将函数结果和response中的内容一并发送给大模型
    # tools = [get_weather, get_date_time]
    # tools_map = {tool.name: tool for tool in tools}
    # message = [
    #     HumanMessage(content="成都今天的天气如何？现在是几点了？")
    # ]
    # deep_seek_v3_with_tools = deep_seek_v3_model_init.bind_tools(
    #     [
    #         get_weather,
    #         get_date_time,
    #     ]
    # )
    # ai_response = deep_seek_v3_with_tools.invoke(message)
    # 将AI回答的内容添加到上下文message中
    # message.append(ai_response)
    # 调用大模型需要执行的函数
    # if ai_response.tool_calls:
    #     for tool_call in ai_response.tool_calls:
    #         # 获取到工具名称
    #         tool_name = tool_call["name"]
    #         # 如果tool在map中，则进行调用
    #         if tool_name in tools_map:
    #             print("正在自动执行" + tool_name + "工具用于获取对应的数据")
    #             tool_response = tools_map[tool_name].invoke(tool_call)
    #             message.append(tool_response)
    #         else:
    #             print("不存在名为" + tool_name + "的工具")
    # 将各种回答整合在一起发送给大模型，得到最终结果
    # final_response = deep_seek_v3_with_tools.invoke(message)
    # print(final_response.content)

    # **结构化输出**，为了让大模型输出的结果具有规范性，我们可以使用该机制，其提供多种结构进行输出
    # Pydantic格式: 适合的场景最多
    # class Movie(BaseModel):
    #     """A movie with details."""
    #     title: str = Field(..., description="The title of the movie")
    #     year: int = Field(..., description="The year the movie was released")
    #     director: str = Field(..., description="The director of the movie")
    #     rating: float = Field(..., description="The movie's rating out of 10")
    # deep_seek_v3_model_with_struct = deep_seek_v3_model_init.with_structured_output(Movie)
    # movie_information = deep_seek_v3_model_with_struct.invoke("提供《泰坦尼克号》这部电影的详细信息")
    # print(movie_information)
    # TypedDict格式: 适合不需要运行时验证的场景，比上一种方式更简单
    # class MovieDict(TypedDict):
    #     """A movie with details."""
    #     title: Annotated[str, ..., "The title of the movie"]
    #     year: Annotated[int, ..., "The year the movie was released"]
    #     director: Annotated[str, ..., "The director of the movie"]
    #     rating: Annotated[float, ..., "The movie's rating out of 10"]
    #
    # model_with_structure = deep_seek_v3_model_init.with_structured_output(MovieDict)
    # response = model_with_structure.invoke("Provide details about the movie Inception")
    # print(response)
    # Json模式
    # json_schema = {
    #     "title": "Movie",
    #     "description": "A movie with details",
    #     "type": "object",
    #     "properties": {
    #         "title": {
    #             "type": "string",
    #             "description": "The title of the movie"
    #         },
    #         "year": {
    #             "type": "integer",
    #             "description": "The year the movie was released"
    #         },
    #         "director": {
    #             "type": "string",
    #             "description": "The director of the movie"
    #         },
    #         "rating": {
    #             "type": "number",
    #             "description": "The movie's rating out of 10"
    #         }
    #     },
    #     "required": ["title", "description", "year", "director", "rating"]
    # }
    #
    # model_with_structure = deep_seek_v3_model_init.with_structured_output(
    #     json_schema,
    #     method="json_schema",
    # )
    # response = model_with_structure.invoke("Provide details about the movie Inception")
    # print(response)

    # 大模型的配置文件profile

    # 大模型提示词缓存

    # 大模型提供的服务端工具调用

    # 大模型限速

    # Base URL and Proxy

    # Log probabilities，对于下个词语的自信程度，越接近0越自信

    # Token usage，可以使用回调函数在大模型的回复中统计消耗的token

    # 可以在调用模型时，进行配置属性
    # response = deep_seek_v3_model_init.invoke(
    #     "Tell me a joke",
    #     config={
    #         "run_name": "joke_generation",  # Custom name for this run
    #         "tags": ["humor", "demo"],  # Tags for categorization
    #         "metadata": {"user_id": "123"},  # Custom metadata
    #         "callbacks": [my_callback_handler],  # Callback handlers
    #     }
    # )
    # 配置大模型属性
    # configurable_model = init_chat_model(temperature=0)
    #
    # configurable_model.invoke(
    #     "what's your name",
    #     config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-Nano
    # )
    # configurable_model.invoke(
    #     "what's your name",
    #     config={"configurable": {"model": "claude-sonnet-4-5-20250929"}},  # Run with Claude
    # )
    print("结束Modle学习")