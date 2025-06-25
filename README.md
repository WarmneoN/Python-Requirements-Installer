# Python Requirements Installer

一个自动化Python依赖安装工具，能够自动处理版本兼容性问题，特别适用于不同Python版本间的依赖安装。

## 功能特性

- 自动解析`requirements.txt`文件中的依赖项
- 检测当前Python版本与目标版本的差异
- 当直接安装失败时，自动查找与目标Python版本兼容的最高版本
- 支持复杂的版本约束条件解析

## 使用说明

1. 确保已安装Python 3.x和pip
2. 将本脚本和你的`requirements.txt`文件放在同一目录下
3. 运行脚本：

```bash
# 安装requirements.txt中的所有依赖
python requirements_installer.py
```

## 参数说明

- 默认目标Python版本为3.11
- 脚本会自动检测当前Python版本并给出警告
- 如果直接安装失败，会自动尝试查找兼容版本

## 依赖项

- Python 3.x
- `packaging`库（用于版本比较）

## 注意事项

- 确保有网络连接，脚本需要访问PyPI获取包信息
- 某些特殊包可能无法自动处理，需要手动干预

## 贡献

欢迎提交Issue或Pull Request改进本工具！
