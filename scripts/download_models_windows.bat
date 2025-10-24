@echo off
echo 📥 GAT项目模型下载脚本
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo ❌ 错误: 虚拟环境不存在，请先运行 windows_install.bat
    pause
    exit /b 1
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

echo 📦 安装huggingface-hub...
pip install huggingface-hub

echo.
echo 📥 开始下载基础模型...

REM 创建模型目录
mkdir models\stable-diffusion-v1-5 2>nul
mkdir models\controlnet\canny 2>nul
mkdir data\models 2>nul

echo.
echo 🔄 下载Stable Diffusion基础模型...
echo 这可能需要几分钟，请耐心等待...
huggingface-cli download runwayml/stable-diffusion-v1-5 --local-dir models/stable-diffusion-v1-5

echo.
echo 🔄 下载ControlNet Canny模型...
huggingface-cli download lllyasviel/sd-controlnet-canny --local-dir models/controlnet/canny

echo.
echo ✅ 基础模型下载完成！
echo.
echo 📋 下一步: 下载LoRA模型
echo 运行: scripts\download_lora.bat
echo 或者: python scripts\setup_lora.py
echo.

echo 🎯 完整安装流程:
echo 1. 基础模型 ✅
echo 2. LoRA模型 ⏳ (需要手动下载)
echo 3. 启动项目 🚀
echo.

pause