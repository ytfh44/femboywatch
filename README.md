# 男娘家园

一个展示游戏中可爱男娘角色的网站，使用 Flask + React 构建。

## 功能特点

- 浏览游戏中的男娘角色
- 按类别筛选游戏
- 搜索特定游戏或角色
- 查看男娘数量和可爱度评分
- 添加新游戏和角色

## 技术栈

### 后端
- Flask
- SQLAlchemy
- SQLite

### 前端
- React
- Tailwind CSS

## 部署步骤

1. 克隆仓库：
```bash
git clone [仓库地址]
cd femboywatch
```

2. 安装后端依赖：
```bash
pip install -r requirements.txt
```

3. 安装前端依赖：
```bash
cd frontend
npm install
```

4. 构建前端：
```bash
npm run build
```

5. 初始化数据库：
```bash
python init_db.py
```

6. 启动服务器：
```bash
python -m flask run
```

## 部署选项

### Heroku 部署
1. 创建 Heroku 账号
2. 安装 Heroku CLI
3. 登录 Heroku：
```bash
heroku login
```
4. 创建应用：
```bash
heroku create your-app-name
```
5. 推送代码：
```bash
git push heroku main
```

### 其他部署选项
- Vercel
- Railway
- PythonAnywhere
- DigitalOcean

## 开发说明

- 后端API位于 `app.py`
- 数据库模型在 `database.py`
- 前端代码在 `frontend/src` 目录下
- 使用 `flask run` 启动开发服务器
- 使用 `npm start` 启动前端开发服务器

## 许可证

MIT
