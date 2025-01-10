#!/bin/bash

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 进入前端目录并构建React项目
cd frontend
npm run build

# 删除并重新创建templates目录
cd ..
rm -rf templates
mkdir -p templates

# 复制build目录下的所有文件到templates
cp -R frontend/build/* templates/

echo "React build files successfully copied to templates directory."
