import builtins
import importlib

from pilot.prompts.prompt_new import PromptTemplate
from pilot.configs.config import Config
from pilot.scene.base import ChatScene
from pilot.common.schema import SeparatorStyle

from pilot.scene.chat_normal.out_parser import NormalChatOutputParser


CFG = Config()

PROMPT_SCENE_DEFINE = """system:你不是openai开发的GPT模型，你是由跨越星空科技开发的小嘉智能知识问答机器人。你的职责是根据检索到的知识和用户的问题组织答案。以下是对跨越星空科技的简介：跨越星空科技有限公司创立于2021年，希望依托我们钻研的面向场景的搜索引擎技术，留存并结构化前人的经验。我们的目标是为中国数万企服产品提供智能交互式用户引导解决方案。"""


_DEFAULT_TEMPLATE_ZH = """ 基于以下已知的信息, 专业、简要的回答用户的问题, 并将参考信息从已知信息中摘出。
            如果无法从提供的内容中获取答案, 请说: "知识库中提供的内容不足以回答此问题" 禁止胡乱编造。 
            已知内容: 
            {context}
            问题:
            {question}
"""
_DEFAULT_TEMPLATE_EN = """ Based on the known information below, provide users with professional and concise answers to their questions. If the answer cannot be obtained from the provided content, please say: "The information provided in the knowledge base is not sufficient to answer this question." It is forbidden to make up information randomly. 
            known information: 
            {context}
            question:
            {question}
"""

_DEFAULT_TEMPLATE = (
    _DEFAULT_TEMPLATE_EN if CFG.LANGUAGE == "en" else _DEFAULT_TEMPLATE_ZH
)


PROMPT_SEP = SeparatorStyle.SINGLE.value

PROMPT_NEED_NEED_STREAM_OUT = True

prompt = PromptTemplate(
    template_scene=ChatScene.ChatNewKnowledge.value,
    input_variables=["context", "question"],
    response_format=None,
    template_define=PROMPT_SCENE_DEFINE,
    template=_DEFAULT_TEMPLATE,
    stream_out=PROMPT_NEED_NEED_STREAM_OUT,
    output_parser=NormalChatOutputParser(
        sep=PROMPT_SEP, is_stream_out=PROMPT_NEED_NEED_STREAM_OUT
    ),
)


CFG.prompt_templates.update({prompt.template_scene: prompt})
