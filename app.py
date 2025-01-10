import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 导入数据库相关模块
from database import init_db, seed_initial_data, db, Project

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# 初始化数据库
init_db(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/hello')
def hello():
    return {"message": "Hello from Flask!"}

@app.route('/api/search', methods=['GET'])
def search():
    """
    搜索API端点，支持多种搜索方式
    查询参数：
    - q: 搜索关键词
    - category: 可选的类别过滤
    """
    query = request.args.get('q', '').lower()
    category = request.args.get('category')

    # 如果没有搜索词，返回空结果
    if not query:
        return jsonify({"results": [], "total": 0})

    # 构建查询
    search_query = Project.query

    # 按关键词搜索
    if query:
        search_query = search_query.filter(
            (Project.title.ilike(f'%{query}%')) | 
            (Project.description.ilike(f'%{query}%')) | 
            (Project.keywords.ilike(f'%{query}%'))
        )

    # 按类别过滤
    if category:
        search_query = search_query.filter(Project.category == category)

    # 执行查询并转换结果
    results = [project.to_dict() for project in search_query.all()]

    return jsonify({
        "results": results,
        "total": len(results)
    })

@app.route('/api/database', methods=['GET', 'POST'])
def get_database_items():
    """
    获取或添加数据库项目
    GET: 获取列表，支持类别过滤
    POST: 添加新游戏
    """
    if request.method == 'GET':
        category = request.args.get('category')
        query = Project.query
        if category:
            query = query.filter(Project.category == category)
        results = [project.to_dict() for project in query.all()]
        return jsonify(results)
    
    elif request.method == 'POST':
        try:
            data = request.json
            new_project = Project(
                title=data['title'],
                category=data['category'],
                description=data['description'],
                full_description=data['fullDescription'],
                keywords=','.join(data['keyPoints']),
                research_team=','.join(data['researchTeam']),
                funding_source=data['femboyCount'],
                cuteness=data['cuteness']
            )
            db.session.add(new_project)
            db.session.commit()
            return jsonify(new_project.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/database/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_database_item(item_id):
    """
    管理特定ID的数据库项目
    GET: 获取详情
    PUT: 更新
    DELETE: 删除
    """
    project = Project.query.get_or_404(item_id)
    
    if request.method == 'GET':
        return jsonify(project.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = request.json
            project.title = data.get('title', project.title)
            project.category = data.get('category', project.category)
            project.description = data.get('description', project.description)
            project.full_description = data.get('fullDescription', project.full_description)
            project.keywords = ','.join(data.get('keyPoints', project.keywords.split(',')))
            project.research_team = ','.join(data.get('researchTeam', project.research_team.split(',')))
            project.funding_source = data.get('femboyCount', project.funding_source)
            project.cuteness = data.get('cuteness', project.cuteness)
            db.session.commit()
            return jsonify(project.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(project)
            db.session.commit()
            return '', 204
        except Exception as e:
            return jsonify({'error': str(e)}), 400

# 确保React路由也能正常工作
@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory(app.static_folder, 'index.html')

# 应用启动时初始化数据
with app.app_context():
    seed_initial_data(app)

if __name__ == '__main__':
    app.run(debug=True)
