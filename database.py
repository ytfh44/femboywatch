import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import JSON
from datetime import date

# 设置控制台编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 项目模型
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    full_description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.Text, nullable=True)
    research_team = db.Column(db.Text, nullable=True)
    funding_source = db.Column(db.Integer, nullable=True)  # 男娘数量
    cuteness = db.Column(db.Integer, nullable=True)  # 可爱度

    # 新增持久化字段
    femboy_characters = db.Column(JSON, nullable=True)  # 存储男娘角色详情
    game_tags = db.Column(db.Text, nullable=True)  # 游戏标签
    release_date = db.Column(db.Date, nullable=True)  # 发行日期
    developer = db.Column(db.String(200), nullable=True)  # 开发商
    platforms = db.Column(db.Text, nullable=True)  # 支持平台
    age_rating = db.Column(db.String(50), nullable=True)  # 年龄分级
    price = db.Column(db.Float, nullable=True)  # 价格
    discount = db.Column(db.Float, nullable=True)  # 折扣
    
    # 时间戳
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'details': {
                'fullDescription': self.full_description,
                'keyPoints': self.keywords.split(',') if self.keywords else [],
                'researchTeam': self.research_team.split(',') if self.research_team else [],
                'femboyCount': self.funding_source,
                'cuteness': self.cuteness,
                'femboyCharacters': self.femboy_characters or [],
                'gameTags': self.game_tags.split(',') if self.game_tags else [],
                'releaseDate': str(self.release_date) if self.release_date else None,
                'developer': self.developer,
                'platforms': self.platforms.split(',') if self.platforms else [],
                'ageRating': self.age_rating,
                'price': self.price,
                'discount': self.discount
            }
        }

def init_db(app):
    """
    初始化数据库
    """
    # 配置SQLite数据库路径
    db_path = os.path.join(os.path.dirname(app.instance_path or '.'), 'projects.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

def seed_initial_data(app):
    """
    填充初始数据
    """
    with app.app_context():
        # 检查是否已有数据
        if Project.query.count() == 0:
            initial_projects = [
                Project(
                    title='可爱男娘RPG',
                    category='角色扮演',
                    description='一款以男娘为主角的奇幻RPG游戏',
                    full_description='探索一个充满魔法和冒险的世界，扮演独特的男娘角色，体验非凡的旅程。',
                    keywords='男娘,RPG,奇幻,冒险',
                    research_team='YTF工作室',
                    funding_source=10,
                    cuteness=9,
                    femboy_characters=[
                        {
                            'name': '小樱',
                            'age': 18,
                            'description': '可爱的男娘法师',
                            'abilities': ['魔法', '治疗']
                        }
                    ],
                    game_tags='奇幻,RPG,男娘',
                    release_date=date(2024, 6, 15),
                    developer='YTF工作室',
                    platforms='PC,Switch',
                    age_rating='15+',
                    price=39.99,
                    discount=0.2
                ),
                Project(
                    title='男娘恋爱模拟器',
                    category='恋爱模拟',
                    description='一款充满爱意的男娘恋爱游戏',
                    full_description='在这个温馨的恋爱世界中，与可爱的男娘角色建立深厚的感情。',
                    keywords='男娘,恋爱,模拟',
                    research_team='萌系工作室',
                    funding_source=15,
                    cuteness=10,
                    femboy_characters=[
                        {
                            'name': '小樱花',
                            'age': 19,
                            'description': '害羞的男娘学生',
                            'abilities': ['甜美', '温柔']
                        }
                    ],
                    game_tags='恋爱,模拟,治愈',
                    release_date=date(2024, 8, 20),
                    developer='萌系工作室',
                    platforms='PC,PS4',
                    age_rating='18+',
                    price=49.99,
                    discount=0.1
                )
            ]
            
            db.session.add_all(initial_projects)
            db.session.commit()
