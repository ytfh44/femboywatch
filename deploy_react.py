import os
import shutil
import subprocess

def deploy_react():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 切换到前端目录并构建React项目
    frontend_dir = os.path.join(script_dir, 'frontend')
    os.chdir(frontend_dir)
    subprocess.run(['npm', 'run', 'build'], check=True)
    
    # 删除并重新创建templates目录
    templates_dir = os.path.join(script_dir, 'templates')
    if os.path.exists(templates_dir):
        shutil.rmtree(templates_dir)
    os.makedirs(templates_dir)
    
    # 复制build目录下的所有文件到templates
    build_dir = os.path.join(frontend_dir, 'build')
    for item in os.listdir(build_dir):
        source = os.path.join(build_dir, item)
        destination = os.path.join(templates_dir, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    
    print("React build files successfully copied to templates directory.")

if __name__ == '__main__':
    deploy_react()
