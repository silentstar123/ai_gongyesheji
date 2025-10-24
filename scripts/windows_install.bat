@echo off
echo 🚀 GAT - AI辅助工业设计项目 Windows安装脚本
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8-3.11
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装
python --version

REM 检查CUDA是否安装
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告: 未检测到NVIDIA GPU或CUDA未安装
    echo 建议安装CUDA Toolkit: https://developer.nvidia.com/cuda-downloads
    echo 继续安装但可能无法使用GPU加速...
    pause
) else (
    echo ✅ 检测到NVIDIA GPU
    nvidia-smi
)

echo.
echo 📦 开始安装项目依赖...

REM 创建虚拟环境
echo 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo ❌ 虚拟环境创建失败
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装PyTorch (CUDA版本)
echo 安装PyTorch (CUDA版本)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM 安装其他依赖
echo 安装项目依赖...
pip install diffusers transformers accelerate safetensors opencv-python Pillow numpy scipy streamlit gradio fastapi uvicorn tqdm click pyyaml python-dotenv requests

REM 安装xformers (可选，用于优化)
echo 安装xformers优化...
pip install xformers

REM 创建必要目录
echo 创建项目目录...
mkdir data\input 2>nul
mkdir data\output 2>nul
mkdir data\models 2>nul
mkdir data\materials 2>nul
mkdir models 2>nul
mkdir logs 2>nul

echo.
echo ✅ 安装完成！
echo.
echo 🎯 下一步操作：
echo 1. 下载Morphy Richards LoRA模型到 data\models\
echo 2. 下载Stable Diffusion基础模型到 models\stable-diffusion-v1-5\
echo 3. 运行: python src\main.py --mode ui
echo.
echo 📋 模型下载地址：
echo - LoRA模型: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
echo - 基础模型: https://huggingface.co/runwayml/stable-diffusion-v1-5
echo.
echo 🔗 项目链接: https://github.com/GINHE527/GAT
echo.

pause
