@echo off
echo 📥 下载Morphy Richards LoRA模型
echo.

REM 检查目标目录
if not exist "data\models" (
    echo 📁 创建模型目录...
    mkdir data\models
)

REM 检查文件是否已存在
if exist "data\models\morphyrichards_home_appliances.safetensors" (
    echo ✅ LoRA模型文件已存在
    echo 文件路径: data\models\morphyrichards_home_appliances.safetensors
    echo 文件大小: 
    dir "data\models\morphyrichards_home_appliances.safetensors" | findstr "morphyrichards_home_appliances.safetensors"
    echo.
    echo 是否重新下载? (y/n)
    set /p choice=
    if /i "%choice%" neq "y" exit /b 0
)

echo.
echo 📋 请手动下载Morphy Richards LoRA模型:
echo.
echo 1. 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
echo 2. 点击 "Download" 按钮
echo 3. 下载文件: morphy_richards_home_appliances.safetensors (144.11 MB)
echo 4. 将文件保存到: data\models\morphyrichards_home_appliances.safetensors
echo.
echo 💡 提示: 需要注册Civitai账户才能下载
echo.

echo 下载完成后，按任意键继续...
pause >nul

REM 检查文件是否已下载
if exist "data\models\morphyrichards_home_appliances.safetensors" (
    echo ✅ LoRA模型下载完成！
    echo 文件路径: data\models\morphyrichards_home_appliances.safetensors
    echo.
    echo 🚀 现在可以启动项目了:
    echo scripts\run_project.bat
) else (
    echo ❌ 未找到LoRA模型文件
    echo 请确保文件已下载到正确位置
)

echo.
pause
