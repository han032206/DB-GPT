from flask import Flask, request
import sys
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)
from pilot.configs.config import Config
import os
from pilot.configs.model_config import (
    DATASETS_DIR,
    KNOWLEDGE_UPLOAD_ROOT_PATH,
    LOGDIR,
    LLM_MODEL_CONFIG,
)
import shutil
from pilot.source_embedding.knowledge_embedding import KnowledgeEmbedding
vector_store_name = {"vs_name": ""}
CFG = Config()
from pilot.utils import build_logger
logger = build_logger("webserver", LOGDIR + "webserver.log")

app = Flask(__name__)

# 定义 knowledge embedding 函数，需要根据具体情况进行修改
def knowledge_embedding_store(vs_id, files):
    # vs_path = os.path.join(VS_ROOT_PATH, vs_id)
    if not os.path.exists(os.path.join(KNOWLEDGE_UPLOAD_ROOT_PATH, vs_id)):
        os.makedirs(os.path.join(KNOWLEDGE_UPLOAD_ROOT_PATH, vs_id))
    for file in files:
        filename = os.path.split(file.name)[-1]
        shutil.move(
            file.name, os.path.join(KNOWLEDGE_UPLOAD_ROOT_PATH, vs_id, filename)
        )
        knowledge_embedding_client = KnowledgeEmbedding(
            file_path=os.path.join(KNOWLEDGE_UPLOAD_ROOT_PATH, vs_id, filename),
            model_name=LLM_MODEL_CONFIG[CFG.EMBEDDING_MODEL],
            vector_store_config={
                "vector_store_name": vector_store_name["vs_name"],
                "vector_store_path": KNOWLEDGE_UPLOAD_ROOT_PATH,
            },
        )
        knowledge_embedding_client.knowledge_embedding()

    logger.info("knowledge embedding success")
    return vs_id

def save_vs_name(vs_name):
    vector_store_name["vs_name"] = vs_name
    return vs_name


# 定义接口路由
@app.route('/api/embedding', methods=['POST'])
def embedding():
    # 获取请求参数
    group = request.form.get('group')
    file = request.files['file']

    # 按用户组名字命名数据库
    db_name = 'embedding_' + group

    if not os.path.exists(os.path.join(DATASETS_DIR, db_name)):
        os.makedirs(os.path.join(DATASETS_DIR, db_name))
    # save the file to the directory
    file.save(os.path.join(DATASETS_DIR, db_name, file.filename))

    files = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(DATASETS_DIR, db_name)):
        files.append(os.path.join(dirpath,dirnames,filenames))


    db_name = save_vs_name(db_name)
    # 调用 knowledge embedding 函数进行处理
    embedding_data = knowledge_embedding_store(db_name, files)

    # 将处理后的数据插入数据库

    # 返回处理后的数据
    return 'knowledge embedding success'

if __name__ == '__main__':
    app.run(debug=True)