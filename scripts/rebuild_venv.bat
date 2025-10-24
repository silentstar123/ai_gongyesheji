@echo off
echo 🔧 重建虚拟环境脚本
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.8-3.11
    pause
    exit /b 1
)

REM 删除旧虚拟环境
if exist "venv" (
    echo 🗑️  删除旧虚拟环境...
    rmdir /s /q venv
)

REM 创建新虚拟环境
echo 📦 创建新虚拟环境...
python -m venv venv

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo ⬆️  升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 📚 安装项目依赖...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate safetensors opencv-python Pillow numpy scipy streamlit gradio fastapi uvicorn tqdm click pyyaml python-dotenv requests xformers

echo.
echo ✅ 虚拟环境重建完成！
echo.
echo 🎯 现在可以运行项目了:
echo python src\main.py --mode ui
echo.

pause
