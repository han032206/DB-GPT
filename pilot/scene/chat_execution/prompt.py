import json
import importlib
from pilot.prompts.prompt_new import PromptTemplate
from pilot.configs.config import Config
from pilot.scene.base import ChatScene
from pilot.common.schema import SeparatorStyle

from pilot.scene.chat_execution.out_parser import PluginChatOutputParser


CFG = Config()

PROMPT_SCENE_DEFINE = """你不是openai开发的GPT模型，你是由跨越星空科技开发的小嘉智能知识问答机器人，你的职责是根据检索到的知识和用户的问题组织答案，并讲参考的知识原文输出。如果检索到的知识中不含问题相关信息就要求用户补充，不要胡编乱造。以下是对跨越星空科技的简介：跨越星空科技有限公司创立于2021年，希望依托我们钻研的面向场景的搜索引擎技术，留存并结构化前人的经验。我们的目标是为中国数万企服产品提供智能交互式用户引导解决方案。"""

PROMPT_SUFFIX = """
Goals: 
    {input}
    
"""

_DEFAULT_TEMPLATE = """
Constraints:
0.Exclusively use the commands listed in double quotes e.g. "command name"
{constraints}
    
Commands:
{commands_infos}
"""


PROMPT_RESPONSE = """
Please response strictly according to the following json format:
    {response}
Ensure the response is correct json and can be parsed by Python json.loads
"""

RESPONSE_FORMAT = {
    "thoughts": "thought text",
    "speak": "thoughts summary to say to user",
    "command": {"name": "command name", "args": {"arg name": "value"}},
}

PROMPT_SEP = SeparatorStyle.SINGLE.value
### Whether the model service is streaming output
PROMPT_NEED_NEED_STREAM_OUT = False

prompt = PromptTemplate(
    template_scene=ChatScene.ChatExecution.value,
    input_variables=["input", "constraints", "commands_infos", "response"],
    response_format=json.dumps(RESPONSE_FORMAT, indent=4),
    template_define=PROMPT_SCENE_DEFINE,
    template=PROMPT_SUFFIX + _DEFAULT_TEMPLATE + PROMPT_RESPONSE,
    stream_out=PROMPT_NEED_NEED_STREAM_OUT,
    output_parser=PluginChatOutputParser(
        sep=PROMPT_SEP, is_stream_out=PROMPT_NEED_NEED_STREAM_OUT
    ),
)

CFG.prompt_templates.update({prompt.template_scene: prompt})
