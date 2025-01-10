import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

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
                'cuteness': self.cuteness
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
    # 检查是否已有数据
    if Project.query.count() == 0:
        initial_projects = [
            Project(
                title='原神',
                category='开放世界',
                description='提瓦特大陆的男娘冒险',
                full_description='在提瓦特大陆的冒险中，玩家可以遇到温迪、行秋等多位可爱的男娘角色。每个角色都有独特的性格和故事，让人不禁想要收集更多。',
                keywords='温迪,行秋,重云,赛诺',
                research_team='米哈游,原神制作组',
                funding_source=4,  # 男娘数量
                cuteness=95  # 可爱度
            ),
            Project(
                title='崩坏：星穹铁道',
                category='回合策略',
                description='星穹列车上的男娘冒险',
                full_description='在开拓星穹铁道的旅程中，丹恒、阿兰等男娘角色陪伴玩家探索未知。每个角色都设计精美，性格鲜明。',
                keywords='丹恒,阿兰,黄泉',
                research_team='米哈游,星穹铁道制作组',
                funding_source=3,  # 男娘数量
                cuteness=90  # 可爱度
            ),
            Project(
                title='明日方舟',
                category='塔防',
                description='罗德岛的男娘干员们',
                full_description='在感染者与非感染者的故事中，安赛尔、巫恋等男娘干员们活跃在第一线。他们不仅战斗力出众，更是可爱到让人忍不住想要护住。',
                keywords='安赛尔,巫恋,菲亚梅塔',
                research_team='鹰角网络,方舟制作组',
                funding_source=5,  # 男娘数量
                cuteness=88  # 可爱度
            )
        ]
        
        db.session.add_all(initial_projects)
        db.session.commit()
        print("初始数据已成功写入数据库")
    else:
        print("数据库已包含数据，跳过初始化")
