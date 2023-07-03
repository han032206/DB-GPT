from flask import Flask, request

app = Flask(__name__)

# 定义 knowledge embedding 函数，需要根据具体情况进行修改
def knowledge_embedding(group, data_path):
    # 对数据进行 knowledge embedding 处理
    pass

# 定义接口路由
@app.route('/api/embedding', methods=['POST'])
def embedding():
    # 获取请求参数
    group = request.form.get('group')
    data_path = request.form.get('data_path')

    # 调用 knowledge embedding 函数进行处理
    embedding_data = knowledge_embedding(group, data_path)

    # 按用户组名字命名数据库
    db_name = 'embedding_' + group

    # 连接 MongoDB 数据库
    client = pymongo.MongoClient()
    db = client[db_name]

    # 将处理后的数据插入数据库
    db.embedding_data.insert_one(embedding_data)

    # 设置数据库为待检索状态
    db.command('enablesharding', db_name)

    # 返回处理后的数据
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)