@echo off
REM 切换到项目根目录
cd /d %~dp0

REM 进入前端目录并构建React项目
cd frontend
npm run build

REM 清空templates目录
cd ..
if exist templates (
    rmdir /s /q templates
)
mkdir templates

REM 复制build目录下的所有文件到templates
xcopy /E /I frontend\build templates

echo React build files successfully copied to templates directory.
pause
