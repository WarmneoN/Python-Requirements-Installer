import subprocess
import re
import sys
from packaging import version

def get_python_version():
    """获取当前Python版本"""
    return f"{sys.version_info.major}.{sys.version_info.minor}"

def parse_requirements(file_path):
    """解析requirements.txt文件"""
    requirements = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                # 移除注释部分
                line = line.split('#')[0].strip()
                requirements.append(line)
    return requirements

def extract_package_info(req):
    """从需求字符串中提取包名和版本约束"""
    # 使用正则表达式匹配包名和版本
    match = re.match(r'([a-zA-Z0-9-_]+)([><=!~]=?.*)?', req)
    if not match:
        return None, None
    
    package = match.group(1)
    version_spec = match.group(2).strip() if match.group(2) else ''
    return package, version_spec

def find_compatible_version(package, target_python="3.11"):
    """查找与目标Python版本兼容的最高版本"""
    try:
        # 使用pip index命令获取所有可用版本
        cmd = [sys.executable, "-m", "pip", "index", "versions", package]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 解析输出以获取所有版本
        versions_line = next(line for line in result.stdout.split('\n') if "Available versions:" in line)
        versions_str = versions_line.split("Available versions:")[1].strip()
        all_versions = [v.strip() for v in versions_str.split(',')]
        
        # 获取包的元数据来检查Python版本兼容性
        compatible_versions = []
        for v in all_versions:
            try:
                cmd = [sys.executable, "-m", "pip", "download", "--no-deps", f"{package}=={v}", "--dry-run"]
                subprocess.run(cmd, capture_output=True, check=True)
                compatible_versions.append(v)
            except subprocess.CalledProcessError:
                continue
        
        if not compatible_versions:
            return None
        
        # 返回最高版本
        return max(compatible_versions, key=version.parse)
    
    except Exception as e:
        print(f"Error finding compatible version for {package}: {str(e)}")
        return None

def install_requirements(requirements_file):
    """安装requirements.txt中的依赖，处理版本兼容问题"""
    current_python = get_python_version()
    target_python = "3.11"
    
    if current_python != target_python:
        print(f"警告: 当前Python版本是{current_python}, 但目标版本是{target_python}")
    
    requirements = parse_requirements(requirements_file)
    
    for req in requirements:
        package, version_spec = extract_package_info(req)
        if not package:
            continue
        
        print(f"\n正在处理包: {package}{version_spec if version_spec else ''}")
        
        try:
            # 尝试安装原始版本
            cmd = [sys.executable, "-m", "pip", "install", req]
            subprocess.run(cmd, check=True)
            print(f"成功安装: {req}")
        except subprocess.CalledProcessError:
            print(f"安装失败: {req}, 正在查找兼容版本...")
            
            # 查找兼容版本
            compatible_version = find_compatible_version(package, target_python)
            if compatible_version:
                print(f"找到兼容版本: {package}=={compatible_version}")
                try:
                    cmd = [sys.executable, "-m", "pip", "install", f"{package}=={compatible_version}"]
                    subprocess.run(cmd, check=True)
                    print(f"成功安装兼容版本: {package}=={compatible_version}")
                except subprocess.CalledProcessError as e:
                    print(f"安装兼容版本失败: {str(e)}")
            else:
                print(f"无法找到与Python {target_python}兼容的{package}版本")

if __name__ == "__main__":
    requirements_file = "requirements.txt"
    print(f"开始安装 {requirements_file} 中的依赖...")
    install_requirements(requirements_file)
    print("\n安装过程完成!")