@echo off
echo 🚀 GAT项目快速启动
echo.

REM 检查是否已安装
if not exist "venv\Scripts\activate.bat" (
    echo 📦 首次运行，开始安装...
    call scripts\windows_install.bat
    if errorlevel 1 (
        echo ❌ 安装失败
        pause
        exit /b 1
    )
)

REM 检查模型
if not exist "data\models\morphy_richards_home_appliances.safetensors" (
    echo 📥 下载模型...
    call scripts\download_models_windows.bat
    echo.
    echo ⚠️  请手动下载Morphy Richards LoRA模型:
    echo 1. 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
    echo 2. 下载文件保存到: data\models\morphy_richards_home_appliances.safetensors
    echo.
    pause
)

echo 🎯 启动项目...
call scripts\run_project.bat
