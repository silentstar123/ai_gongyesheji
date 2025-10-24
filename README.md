# GAT - AI辅助工业设计项目

## 项目简介

GAT (GINHE AI Technology) 是一个基于AI的工业设计自动化系统，实现从CAD线稿到写实工业风格图像的智能转换，并支持自动材质分配和3D交互编辑。

## 核心功能

- **CAD到AI渲染转换**: 将CAD六视图线稿转换为写实工业风格图像
- **智能材质分配**: 使用MatCLIP进行自动材质匹配
- **3D交互编辑**: 支持全角度交互和局部材质编辑
- **模型持续优化**: 通过用户反馈进行模型重训练

## 技术架构

- **基础模型**: OpenVINO SD 1.5 INT8
- **控制模块**: T2I-Adapter (Sketch/Canny/Depth)
- **风格模型**: 各种写实工业风格LoRA
- **运行时**: UE5 NNE + ONNX Runtime

## 项目结构

```
GAT/
├── docs/                    # 项目文档
├── src/                     # 源代码
├── models/                  # AI模型文件
├── data/                    # 数据文件
├── configs/                 # 配置文件
├── tests/                   # 测试文件
└── README.md               # 项目说明
```

## 快速开始

### Windows用户（推荐）

#### 方法1：一键启动（最简单）
```bash
# 1. 克隆项目
git clone https://github.com/GINHE527/GAT.git
cd GAT

# 2. 一键启动（自动安装+下载模型+启动）
scripts\quick_start.bat
```

#### 方法2：分步安装
```bash
# 1. 克隆项目
git clone https://github.com/GINHE527/GAT.git
cd GAT

# 2. 安装依赖
scripts\windows_install.bat

# 3. 下载模型
scripts\download_models_windows.bat

# 4. 手动下载LoRA模型
# 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
# 下载到: data\models\morphy_richards_home_appliances.safetensors

# 5. 启动项目
scripts\run_project.bat
```

#### 方法3：直接运行
```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动Web界面
python src\main.py --mode ui
```

### Linux/Mac用户
1. **克隆仓库**
```bash
git clone https://github.com/GINHE527/GAT.git
cd GAT
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境**
```bash
cp configs/config.example.yaml configs/config.yaml
# 编辑配置文件
```

4. **运行项目**
```bash
python src/main.py
```

## 开发计划

详细的项目计划请参考 [AI辅助工业设计项目计划.md](./AI辅助工业设计项目计划.md)

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目链接: [https://github.com/GINHE527/GAT](https://github.com/GINHE527/GAT)
- 问题反馈: [Issues](https://github.com/GINHE527/GAT/issues)

## 致谢

- 感谢所有贡献者的支持
- 特别感谢Morphy Richards LoRA模型的提供者
- 感谢开源社区的技术支持
