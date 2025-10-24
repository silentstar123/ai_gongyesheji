# GAT 快速开始指南

## 🚀 快速安装

### 1. 克隆项目
```bash
git clone git@github.com:GINHE527/GAT.git
cd GAT
```

### 2. 自动安装
```bash
# 运行安装脚本
chmod +x scripts/install.sh
./scripts/install.sh
```

### 3. 手动安装（可选）
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 📥 下载模型

### 必需模型
1. **Morphy Richards LoRA模型**
   - 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
   - 下载: `morphy_richards_home_appliances.safetensors` (144.11 MB)
   - 保存到: `data/models/morphy_richards_home_appliances.safetensors`

2. **Stable Diffusion基础模型**
   ```bash
   # 使用huggingface-hub下载
   pip install huggingface-hub
   huggingface-cli download runwayml/stable-diffusion-v1-5 --local-dir models/stable-diffusion-v1-5
   ```

3. **ControlNet模型**
   ```bash
   huggingface-cli download lllyasviel/sd-controlnet-canny --local-dir models/controlnet/canny
   ```

## 🎯 使用方法

### 1. Web界面（推荐）
```bash
# 激活虚拟环境
source venv/bin/activate

# 启动Web界面
python src/main.py --mode ui
```

访问: http://localhost:8501

### 2. 命令行模式
```bash
python src/main.py --mode cli \
  --input your_cad_file.png \
  --prompt "home appliance, modern design, white color" \
  --lora morphy_richards \
  --num-images 4
```

### 3. API服务
```bash
python src/main.py --mode api
```

访问: http://localhost:8000

## 🎨 使用示例

### 基本工作流程
1. **上传CAD文件** - 支持PNG, JPG, OBJ, STL等格式
2. **输入提示词** - 描述想要的产品特征
3. **选择LoRA模型** - 使用Morphy Richards风格
4. **生成图像** - 获得4张不同角度的产品图像
5. **下载结果** - 保存生成的图像

### 提示词示例
```
# 基础提示词
"home appliance, modern design, white color, minimalist style"

# 详细提示词
"morphyrichards, home appliance, modern design, white color, 
minimalist style, professional photography, studio lighting, 
high quality, detailed, realistic"

# 负面提示词
"blurry, low quality, distorted, ugly, cartoon, anime"
```

## ⚙️ 配置说明

### 主要配置文件
- `configs/config.yaml` - 主配置文件
- `requirements.txt` - Python依赖
- `setup.py` - 项目安装配置

### 重要参数
- **LoRA权重**: 0.8 (推荐)
- **引导强度**: 7.5 (推荐)
- **推理步数**: 20 (推荐)
- **图像尺寸**: 512x512 (默认)

## 🔧 故障排除

### 常见问题

1. **CUDA内存不足**
   ```bash
   # 在config.yaml中设置
   hardware:
     memory_efficient: true
     use_xformers: true
   ```

2. **模型加载失败**
   - 检查模型文件路径
   - 确认文件完整性
   - 检查文件权限

3. **生成质量不佳**
   - 调整引导强度 (guidance_scale)
   - 增加推理步数 (num_inference_steps)
   - 优化提示词

### 性能优化
- 使用GPU加速
- 启用xformers优化
- 调整批处理大小
- 使用内存优化模式

## 📊 系统要求

### 最低配置
- Python 3.8+
- 8GB RAM
- 10GB 存储空间
- CPU推理支持

### 推荐配置
- Python 3.10+
- 16GB+ RAM
- 20GB+ 存储空间
- NVIDIA GPU (8GB+ VRAM)
- CUDA 11.8+

## 🆘 获取帮助

- **项目文档**: README.md
- **问题反馈**: GitHub Issues
- **技术交流**: QQ群 511020855
- **项目链接**: https://github.com/GINHE527/GAT

## 🎯 下一步

1. **探索更多LoRA模型**
2. **自定义训练LoRA**
3. **集成更多CAD格式**
4. **开发材质系统**
5. **优化生成质量**

---

**祝您使用愉快！** 🎨✨
