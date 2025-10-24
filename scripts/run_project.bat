@echo off
echo 🚀 GAT - AI辅助工业设计项目启动脚本
echo.

REM 检查虚拟环境是否存在
if not exist "venv\Scripts\activate.bat" (
    echo ❌ 错误: 虚拟环境不存在
    echo 请先运行: scripts\windows_install.bat
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查模型文件
if not exist "data\models\morphy_richards_home_appliances.safetensors" (
    echo ⚠️  警告: Morphy Richards LoRA模型未找到
    echo 请下载模型到: data\models\morphy_richards_home_appliances.safetensors
    echo 下载地址: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
    echo.
    echo 是否继续运行? (y/n)
    set /p choice=
    if /i "%choice%" neq "y" exit /b 1
)

if not exist "models\stable-diffusion-v1-5" (
    echo ⚠️  警告: Stable Diffusion基础模型未找到
    echo 请运行: scripts\download_models_windows.bat
    echo.
    echo 是否继续运行? (y/n)
    set /p choice=
    if /i "%choice%" neq "y" exit /b 1
)

echo.
echo 🎯 选择运行模式:
echo 1. Web界面 (推荐)
echo 2. 命令行模式
echo 3. API服务
echo 4. 退出
echo.
set /p mode=请选择 (1-4): 

if "%mode%"=="1" (
    echo 🌐 启动Web界面...
    echo 访问地址: http://localhost:8501
    python src\main.py --mode ui
) else if "%mode%"=="2" (
    echo 💻 启动命令行模式...
    set /p input=请输入CAD文件路径: 
    set /p prompt=请输入提示词: 
    python src\main.py --mode cli --input "%input%" --prompt "%prompt%"
) else if "%mode%"=="3" (
    echo 🔌 启动API服务...
    echo API地址: http://localhost:8000
    python src\main.py --mode api
) else if "%mode%"=="4" (
    echo 👋 再见!
    exit /b 0
) else (
    echo ❌ 无效选择
    pause
    exit /b 1
)

pause
