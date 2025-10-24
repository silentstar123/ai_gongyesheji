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
echo 📥 开始下载模型...

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
echo ⚠️  重要提示：
echo 请手动下载Morphy Richards LoRA模型：
echo 1. 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
echo 2. 下载: morphy_richards_home_appliances.safetensors
echo 3. 保存到: data\models\morphy_richards_home_appliances.safetensors
echo.

echo ✅ 模型下载完成！
echo.
echo 🚀 现在可以启动项目了：
echo python src\main.py --mode ui
echo.

pause
