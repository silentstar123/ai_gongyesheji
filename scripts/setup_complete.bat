@echo off
echo 🎯 GAT项目完整安装和运行指南
echo.

echo 📋 第一步: 安装项目依赖
echo 运行: scripts\windows_install.bat
echo.
echo 📋 第二步: 下载AI模型
echo 运行: scripts\download_models_windows.bat
echo.
echo 📋 第三步: 手动下载LoRA模型
echo 1. 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
echo 2. 下载: morphy_richards_home_appliances.safetensors
echo 3. 保存到: data\models\morphy_richards_home_appliances.safetensors
echo.
echo 📋 第四步: 启动项目
echo 运行: scripts\run_project.bat
echo.
echo 🎯 或者直接运行:
echo python src\main.py --mode ui
echo.

echo 📊 项目结构:
echo GAT\
echo ├── src\                    # 源代码
echo ├── scripts\               # 脚本文件
echo ├── data\models\           # AI模型文件
echo ├── models\                # 基础模型
echo ├── configs\               # 配置文件
echo └── docs\                  # 文档
echo.

echo 🔗 项目链接:
echo - GitHub: https://github.com/GINHE527/GAT
echo - 文档: docs\WINDOWS_SETUP.md
echo.

pause
