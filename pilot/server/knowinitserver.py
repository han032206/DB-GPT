from flask import Flask, request
import os

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
# 定义接口路由
@app.route('/api/embedding', methods=['POST'])
def embedding():
    # 获取请求参数
    group = request.form.get('group')
    data_path = request.form.get('data_path')

    # 调用 knowledge embedding 函数进行处理
    embedding_data = knowledge_embedding_store(group, data_path)

    # 按用户组名字命名数据库
    db_name = 'embedding_' + group

    # 将处理后的数据插入数据库
    

    # 设置数据库为待检索状态
    

    # 返回处理后的数据
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)