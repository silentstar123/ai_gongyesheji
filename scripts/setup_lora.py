"""
Morphy Richards LoRA模型设置脚本
由于文件大小限制，提供多种下载方式
"""

import os
import sys
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm

def check_lora_exists():
    """检查LoRA模型是否已存在"""
    lora_path = Path("data/models/morphyrichards_home_appliances.safetensors")
    if lora_path.exists():
        size_mb = lora_path.stat().st_size / (1024 * 1024)
        print(f"✅ LoRA模型已存在: {lora_path}")
        print(f"📊 文件大小: {size_mb:.1f} MB")
        return True
    return False

def download_from_alternative_source():
    """从备用源下载LoRA模型"""
    print("🔄 尝试从备用源下载LoRA模型...")
    
    # 这里可以添加备用下载链接
    # 由于Civitai需要登录，这里提供指导
    print("📋 请手动下载LoRA模型:")
    print("1. 访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora")
    print("2. 注册/登录Civitai账户")
    print("3. 点击Download按钮")
    print("4. 下载: morphy_richards_home_appliances.safetensors")
    print("5. 保存到: data/models/morphyrichards_home_appliances.safetensors")
    
    return False

def setup_lora_model():
    """设置LoRA模型"""
    print("🎯 Morphy Richards LoRA模型设置")
    print("=" * 50)
    
    # 创建目录
    Path("data/models").mkdir(parents=True, exist_ok=True)
    
    # 检查是否已存在
    if check_lora_exists():
        print("✅ LoRA模型已准备就绪")
        return True
    
    print("❌ LoRA模型未找到")
    print()
    
    # 尝试下载
    if not download_from_alternative_source():
        print()
        print("📝 手动下载步骤:")
        print("1. 打开浏览器访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora")
        print("2. 注册Civitai账户（如果还没有）")
        print("3. 登录后点击'Download'按钮")
        print("4. 下载文件: morphy_richards_home_appliances.safetensors")
        print("5. 将文件移动到: data/models/morphyrichards_home_appliances.safetensors")
        print()
        print("💡 文件大小: 144.11 MB")
        print("💡 文件格式: SafeTensors")
        print("💡 触发词: morphyrichards")
        
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 GAT项目 - LoRA模型设置")
    print()
    
    if setup_lora_model():
        print("🎉 LoRA模型设置完成！")
        print("🚀 现在可以运行项目了:")
        print("   python src/main.py --mode ui")
    else:
        print("⚠️  请按照上述步骤手动下载LoRA模型")
        print("📋 下载完成后，重新运行此脚本验证")

if __name__ == "__main__":
    main()
