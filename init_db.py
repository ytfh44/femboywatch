from flask import Flask
from database import init_db, seed_initial_data, db

# 创建Flask应用
app = Flask(__name__)

def reset_database():
    """
    重置并初始化数据库
    """
    # 配置SQLite数据库路径
    import os
    db_path = os.path.join(os.path.dirname(app.instance_path or '.'), 'projects.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化数据库
    db.init_app(app)

    # 初始化并重置数据库
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_initial_data(app)
        print("数据库已成功重置并填充初始数据")

if __name__ == '__main__':
    reset_database()
