#!/bin/bash

# GAT - AI辅助工业设计项目安装脚本

set -e

echo "🚀 开始安装GAT - AI辅助工业设计项目..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
echo "⬆️ 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt

# 创建必要目录
echo "📁 创建项目目录..."
mkdir -p logs
mkdir -p data/{input,output,models,materials}
mkdir -p models/{stable-diffusion-v1-5,controlnet/{canny,sketch,depth}}

# 设置权限
echo "🔐 设置文件权限..."
chmod +x scripts/*.py
chmod +x scripts/*.sh

# 运行模型下载脚本
echo "📥 准备模型下载..."
python scripts/download_models.py

echo "✅ 安装完成！"
echo ""
echo "🎯 使用方法："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动Web界面: python src/main.py --mode ui"
echo "3. 命令行模式: python src/main.py --mode cli --input your_file.png --prompt 'your prompt'"
echo ""
echo "📋 下一步："
echo "1. 手动下载Morphy Richards LoRA模型到 data/models/"
echo "2. 下载Stable Diffusion基础模型到 models/stable-diffusion-v1-5/"
echo "3. 运行 python src/main.py --mode ui 启动界面"
echo ""
echo "🔗 相关链接："
echo "- LoRA模型: https://civitai.com/models/22932/morphy-richards-home-appliances-lora"
echo "- 基础模型: https://huggingface.co/runwayml/stable-diffusion-v1-5"
echo "- 项目文档: README.md"
