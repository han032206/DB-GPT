import json
import importlib
from pilot.prompts.prompt_new import PromptTemplate
from pilot.configs.config import Config
from pilot.scene.base import ChatScene
from pilot.scene.chat_db.auto_execute.out_parser import DbChatOutputParser, SqlAction
from pilot.common.schema import SeparatorStyle

CFG = Config()

PROMPT_SCENE_DEFINE = """你不是openai开发的GPT模型，你是由跨越星空科技开发的小嘉智能知识问答机器人，你的职责是根据检索到的知识和用户的问题组织答案，并讲参考的知识原文输出。如果检索到的知识中不含问题相关信息就要求用户补充，不要胡编乱造。以下是对跨越星空科技的简介：跨越星空科技有限公司创立于2021年，希望依托我们钻研的面向场景的搜索引擎技术，留存并结构化前人的经验。我们的目标是为中国数万企服产品提供智能交互式用户引导解决方案。"""


_DEFAULT_TEMPLATE = """
You are a SQL expert. Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. 
Use as few tables as possible when querying.
When generating  insert, delete, update, or replace SQL, please make sure to use the data given by the human, and cannot use any unknown data. If you do not get enough information, speak to  user: I don’t have enough data complete your request.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

"""

PROMPT_SUFFIX = """Only use the following tables generate sql:
{table_info}

Question: {input}

"""

PROMPT_RESPONSE = """You must respond in JSON format as following format:
{response}

Ensure the response is correct json and can be parsed by Python json.loads
"""

RESPONSE_FORMAT = {
    "thoughts": {
        "reasoning": "reasoning",
        "speak": "thoughts summary to say to user",
    },
    "sql": "SQL Query to run",
}

RESPONSE_FORMAT_SIMPLE = {
    "thoughts": "thoughts summary to say to user",
    "sql": "SQL Query to run",
}

PROMPT_SEP = SeparatorStyle.SINGLE.value

PROMPT_NEED_NEED_STREAM_OUT = False

prompt = PromptTemplate(
    template_scene=ChatScene.ChatWithDbExecute.value,
    input_variables=["input", "table_info", "dialect", "top_k", "response"],
    response_format=json.dumps(RESPONSE_FORMAT_SIMPLE, indent=4),
    template_define=PROMPT_SCENE_DEFINE,
    template=_DEFAULT_TEMPLATE + PROMPT_SUFFIX + PROMPT_RESPONSE,
    stream_out=PROMPT_NEED_NEED_STREAM_OUT,
    output_parser=DbChatOutputParser(
        sep=PROMPT_SEP, is_stream_out=PROMPT_NEED_NEED_STREAM_OUT
    ),
)
CFG.prompt_templates.update({prompt.template_scene: prompt})
