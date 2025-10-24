# Windows部署指南

## 🖥️ 系统要求

### 硬件要求
- **显卡**: NVIDIA GPU (RTX 3060或更高)
- **显存**: 8GB+ VRAM
- **内存**: 16GB+ RAM
- **存储**: 20GB+ 可用空间

### 软件要求
- **操作系统**: Windows 10/11
- **Python**: 3.8-3.11
- **CUDA**: 11.8或12.1
- **Git**: 最新版本

## 🚀 快速安装

### 1. 安装CUDA Toolkit
```bash
# 下载CUDA Toolkit
# 访问: https://developer.nvidia.com/cuda-downloads
# 选择Windows版本，推荐CUDA 11.8或12.1
```

### 2. 克隆项目
```bash
# 使用Git克隆项目
git clone https://github.com/GINHE527/GAT.git
cd GAT

# 或者下载ZIP文件解压
```

### 3. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows CMD:
venv\Scripts\activate
# Windows PowerShell:
venv\Scripts\Activate.ps1
```

### 4. 安装依赖
```bash
# 升级pip
python -m pip install --upgrade pip

# 安装PyTorch (CUDA版本)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install -r requirements.txt
```

### 5. 下载模型文件

#### 必需模型下载
1. **Morphy Richards LoRA模型**
   - 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora
   - 下载: `morphy_richards_home_appliances.safetensors`
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

### 启动Web界面
```bash
# 激活虚拟环境
venv\Scripts\activate

# 启动Streamlit界面
python src/main.py --mode ui
```

访问: http://localhost:8501

### 命令行使用
```bash
python src/main.py --mode cli --input your_file.png --prompt "home appliance, modern design"
```

### API服务
```bash
python src/main.py --mode api
```

访问: http://localhost:8000

## ⚙️ 配置优化

### GPU优化配置
编辑 `configs/config.yaml`:
```yaml
hardware:
  device: "cuda"  # 使用GPU
  memory_efficient: true
  use_xformers: true  # 启用xformers优化

generation:
  num_inference_steps: 20
  guidance_scale: 7.5
  width: 512
  height: 512
```

### 性能调优
1. **启用xformers优化**
   ```bash
   pip install xformers
   ```

2. **调整批处理大小**
   ```yaml
   generation:
     batch_size: 2  # 根据显存调整
   ```

3. **内存优化**
   ```yaml
   hardware:
     memory_efficient: true
   ```

## 🔧 故障排除

### 常见问题

1. **CUDA内存不足**
   - 减少批处理大小
   - 启用内存优化
   - 降低图像分辨率

2. **模型加载失败**
   - 检查模型文件路径
   - 确认文件完整性
   - 检查网络连接

3. **生成速度慢**
   - 启用xformers
   - 使用GPU加速
   - 调整推理步数

### 性能监控
```bash
# 监控GPU使用情况
nvidia-smi

# 监控内存使用
python -c "import torch; print('GPU可用:', torch.cuda.is_available()); print('GPU数量:', torch.cuda.device_count())"
```

## 📊 推荐配置

### 最低配置
- GPU: RTX 3060 (8GB)
- 内存: 16GB
- 存储: 20GB

### 推荐配置
- GPU: RTX 4070+ (12GB+)
- 内存: 32GB
- 存储: 50GB

### 高性能配置
- GPU: RTX 4090 (24GB)
- 内存: 64GB
- 存储: 100GB

## 🎨 使用示例

### 基本工作流程
1. **上传CAD文件** - 支持PNG, JPG, OBJ等格式
2. **输入提示词** - 描述产品特征
3. **选择LoRA模型** - 使用Morphy Richards风格
4. **生成图像** - 获得高质量产品图像
5. **下载结果** - 保存生成的图像

### 提示词示例
```
# 基础提示词
"morphyrichards, home appliance, modern design, white color, minimalist style"

# 详细提示词
"morphyrichards, home appliance, modern design, white color, 
minimalist style, professional photography, studio lighting, 
high quality, detailed, realistic"

# 负面提示词
"blurry, low quality, distorted, ugly, cartoon, anime"
```

## 🆘 获取帮助

- **项目文档**: README.md
- **问题反馈**: GitHub Issues
- **技术交流**: QQ群 511020855
- **项目链接**: https://github.com/GINHE527/GAT

---

**祝您使用愉快！** 🎨✨
