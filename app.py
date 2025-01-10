import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db, init_db, seed_initial_data, Project
import sqlalchemy.exc

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all API routes

# 初始化数据库
init_db(app)

# 在应用上下文中检查并创建表
def ensure_database_initialized():
    with app.app_context():
        try:
            # 尝试查询是否有表存在
            Project.query.first()
        except sqlalchemy.exc.OperationalError:
            # 如果查询失败（可能是因为表不存在），则创建表
            db.create_all()
            seed_initial_data(app)
        except Exception as e:
            # 处理其他可能的异常
            print(f"初始化数据库时发生错误: {e}")
            db.create_all()
            seed_initial_data(app)

# 在应用启动时确保数据库初始化
ensure_database_initialized()

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
        data = request.json
        
        # 处理详细信息
        details = data.get('details', {})
        
        new_project = Project(
            title=data.get('title', ''),
            category=data.get('category', ''),
            description=data.get('description', ''),
            full_description=details.get('fullDescription', ''),
            keywords=','.join(details.get('keyPoints', [])),
            research_team=','.join(details.get('researchTeam', [])),
            funding_source=details.get('femboyCount', 0),
            cuteness=details.get('cuteness', 0),
            
            # 新增字段
            femboy_characters=details.get('femboyCharacters', []),
            game_tags=','.join(details.get('gameTags', [])),
            release_date=details.get('releaseDate'),
            developer=details.get('developer', ''),
            platforms=','.join(details.get('platforms', [])),
            age_rating=details.get('ageRating', ''),
            price=details.get('price', 0.0),
            discount=details.get('discount', 0.0)
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify(new_project.to_dict()), 201

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
        data = request.json
        
        # 处理详细信息
        details = data.get('details', {})
        
        # 更新基本字段
        project.title = data.get('title', project.title)
        project.category = data.get('category', project.category)
        project.description = data.get('description', project.description)
        project.full_description = details.get('fullDescription', project.full_description)
        project.keywords = ','.join(details.get('keyPoints', project.keywords.split(',') if project.keywords else []))
        project.research_team = ','.join(details.get('researchTeam', project.research_team.split(',') if project.research_team else []))
        project.funding_source = details.get('femboyCount', project.funding_source)
        project.cuteness = details.get('cuteness', project.cuteness)
        
        # 更新新增字段
        project.femboy_characters = details.get('femboyCharacters', project.femboy_characters)
        project.game_tags = ','.join(details.get('gameTags', project.game_tags.split(',') if project.game_tags else []))
        project.release_date = details.get('releaseDate', project.release_date)
        project.developer = details.get('developer', project.developer)
        project.platforms = ','.join(details.get('platforms', project.platforms.split(',') if project.platforms else []))
        project.age_rating = details.get('ageRating', project.age_rating)
        project.price = details.get('price', project.price)
        project.discount = details.get('discount', project.discount)
        
        db.session.commit()
        
        return jsonify(project.to_dict())
    
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

# 主程序入口
if __name__ == '__main__':
    app.run(debug=True)
