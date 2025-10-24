"""
模型下载脚本
自动下载所需的AI模型和LoRA文件
"""

import os
import sys
import requests
import logging
from pathlib import Path
from tqdm import tqdm
import hashlib

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


def download_file(url: str, filepath: Path, expected_hash: str = None) -> bool:
    """
    下载文件
    
    Args:
        url: 下载URL
        filepath: 保存路径
        expected_hash: 期望的MD5哈希值
        
    Returns:
        bool: 下载是否成功
    """
    try:
        # 创建目录
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果文件已存在，检查哈希
        if filepath.exists():
            if expected_hash:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash == expected_hash:
                    logger.info(f"文件已存在且哈希匹配: {filepath}")
                    return True
            else:
                logger.info(f"文件已存在: {filepath}")
                return True
        
        # 下载文件
        logger.info(f"开始下载: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filepath.name) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # 验证哈希
        if expected_hash:
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash != expected_hash:
                logger.error(f"文件哈希不匹配: {filepath}")
                filepath.unlink()  # 删除文件
                return False
        
        logger.info(f"下载完成: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"下载失败: {e}")
        if filepath.exists():
            filepath.unlink()
        return False


def download_morphy_richards_lora():
    """下载Morphy Richards LoRA模型"""
    # 注意：这里需要实际的下载链接
    # 由于Civitai需要登录，这里提供占位符
    lora_info = {
        "name": "morphy_richards_home_appliances",
        "url": "https://civitai.com/api/download/models/27377",  # 需要实际URL
        "filename": "morphy_richards_home_appliances.safetensors",
        "size": "144.11 MB",
        "hash": None  # 需要实际哈希值
    }
    
    filepath = Path("data/models") / lora_info["filename"]
    
    logger.info(f"下载Morphy Richards LoRA模型...")
    logger.warning("注意：需要手动从Civitai下载LoRA模型")
    logger.info(f"请访问: https://civitai.com/models/22932/morphy-richards-home-appliances-lora")
    logger.info(f"下载后保存到: {filepath}")
    
    return True


def download_base_models():
    """下载基础模型"""
    models = [
        {
            "name": "stable-diffusion-v1-5",
            "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5",
            "path": "models/stable-diffusion-v1-5",
            "type": "huggingface"
        },
        {
            "name": "controlnet-canny",
            "url": "https://huggingface.co/lllyasviel/sd-controlnet-canny",
            "path": "models/controlnet/canny",
            "type": "huggingface"
        }
    ]
    
    for model in models:
        logger.info(f"准备下载基础模型: {model['name']}")
        logger.info(f"模型路径: {model['path']}")
        logger.info(f"请手动下载或使用huggingface-hub下载")
    
    return True


def setup_model_directories():
    """创建模型目录结构"""
    directories = [
        "models/stable-diffusion-v1-5",
        "models/controlnet/canny",
        "models/controlnet/sketch", 
        "models/controlnet/depth",
        "data/models",
        "data/materials"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"创建目录: {directory}")


def main():
    """主函数"""
    logging.basicConfig(level=logging.INFO)
    
    logger.info("开始设置GAT项目模型...")
    
    # 创建目录结构
    setup_model_directories()
    
    # 下载基础模型
    download_base_models()
    
    # 下载LoRA模型
    download_morphy_richards_lora()
    
    logger.info("模型设置完成！")
    logger.info("请手动下载以下文件：")
    logger.info("1. Morphy Richards LoRA: https://civitai.com/models/22932/morphy-richards-home-appliances-lora")
    logger.info("2. 基础模型: https://huggingface.co/runwayml/stable-diffusion-v1-5")
    logger.info("3. ControlNet模型: https://huggingface.co/lllyasviel/sd-controlnet-canny")


if __name__ == "__main__":
    main()
