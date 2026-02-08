from dotenv import load_dotenv

from src.utils.models import deep_seek_v3_stream
from src.prompt_template import prompt

load_dotenv()

# message = input("请输入想问AI模型的问题：")

# deep_seek_pro_stream(message)

deep_seek_v3_stream(prompt)

# chain_v3 = deep_seek_v3_chain()
#
# final_chain = prompt | chain_v3
#
# for chunk in final_chain:
#     print(chunk)

