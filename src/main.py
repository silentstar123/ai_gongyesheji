"""
GAT - AI辅助工业设计项目主程序
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.image_generator import ImageGenerator
from src.utils.cad_processor import CADProcessor
from src.ui.streamlit_app import run_streamlit_app

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gat.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def setup_directories():
    """创建必要的目录"""
    directories = [
        'logs',
        'data/input',
        'data/output', 
        'data/models',
        'data/materials',
        'models',
        'configs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"创建目录: {directory}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GAT - AI辅助工业设计项目')
    parser.add_argument('--mode', choices=['ui', 'cli', 'api'], default='ui',
                       help='运行模式: ui(界面), cli(命令行), api(API服务)')
    parser.add_argument('--config', default='configs/config.yaml',
                       help='配置文件路径')
    parser.add_argument('--input', help='输入CAD文件路径')
    parser.add_argument('--output', default='data/output',
                       help='输出目录')
    parser.add_argument('--prompt', help='生成提示词')
    parser.add_argument('--lora', default='morphy_richards',
                       help='使用的LoRA模型')
    parser.add_argument('--num-images', type=int, default=4,
                       help='生成图像数量')
    
    args = parser.parse_args()
    
    try:
        # 设置目录
        setup_directories()
        
        if args.mode == 'ui':
            # 启动Streamlit界面
            logger.info("启动Streamlit界面")
            run_streamlit_app()
            
        elif args.mode == 'cli':
            # 命令行模式
            if not args.input or not args.prompt:
                logger.error("CLI模式需要指定 --input 和 --prompt 参数")
                return
            
            logger.info("启动命令行模式")
            run_cli_mode(args)
            
        elif args.mode == 'api':
            # API服务模式
            logger.info("启动API服务")
            run_api_mode()
            
    except Exception as e:
        logger.error(f"程序运行失败: {e}")
        raise


def run_cli_mode(args):
    """运行命令行模式"""
    try:
        # 初始化图像生成器
        generator = ImageGenerator(args.config)
        
        # 处理CAD输入
        cad_processor = CADProcessor()
        cad_input = cad_processor.load_cad_file(args.input)
        
        # 生成图像
        result = generator.generate_from_cad(
            cad_input=cad_input,
            prompt=args.prompt,
            lora_name=args.lora,
            num_images=args.num_images
        )
        
        # 保存图像
        saved_paths = generator.save_images(
            result['images'],
            args.output,
            prefix=f"generated_{args.lora}"
        )
        
        logger.info(f"生成完成，图像保存在: {args.output}")
        for path in saved_paths:
            print(f"生成图像: {path}")
            
    except Exception as e:
        logger.error(f"CLI模式运行失败: {e}")
        raise


def run_api_mode():
    """运行API服务模式"""
    try:
        from src.api.fastapi_app import create_app
        import uvicorn
        
        app = create_app()
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        logger.error(f"API服务启动失败: {e}")
        raise


def run_streamlit_app():
    """运行Streamlit应用"""
    try:
        import subprocess
        import sys
        
        # 启动Streamlit应用
        cmd = [sys.executable, "-m", "streamlit", "run", "src/ui/streamlit_app.py"]
        subprocess.run(cmd)
        
    except Exception as e:
        logger.error(f"Streamlit应用启动失败: {e}")
        raise


if __name__ == "__main__":
    main()
