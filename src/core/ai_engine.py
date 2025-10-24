"""
AI引擎核心模块
负责管理Stable Diffusion模型、LoRA和ControlNet的集成
"""

import torch
import yaml
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging

from diffusers import StableDiffusionPipeline, ControlNetModel
from transformers import CLIPTextModel, CLIPTokenizer
from safetensors import safe_open

from .lora_manager import LoRAManager
from .controlnet_processor import ControlNetProcessor

logger = logging.getLogger(__name__)


class AIEngine:
    """AI引擎核心类，管理所有AI模型和推理"""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """
        初始化AI引擎
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.device = self._setup_device()
        self.pipeline = None
        self.lora_manager = None
        self.controlnet_processor = None
        
        # 初始化组件
        self._initialize_components()
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise
    
    def _setup_device(self) -> torch.device:
        """设置计算设备"""
        device_config = self.config['hardware']['device']
        
        if device_config == 'auto':
            if torch.cuda.is_available():
                device = torch.device('cuda')
                logger.info(f"使用CUDA设备: {torch.cuda.get_device_name()}")
            elif torch.backends.mps.is_available():
                device = torch.device('mps')
                logger.info("使用MPS设备")
            else:
                device = torch.device('cpu')
                logger.info("使用CPU设备")
        else:
            device = torch.device(device_config)
            
        return device
    
    def _initialize_components(self):
        """初始化所有组件"""
        try:
            # 初始化LoRA管理器
            self.lora_manager = LoRAManager(self.config['models']['lora'])
            
            # 初始化ControlNet处理器
            self.controlnet_processor = ControlNetProcessor(
                self.config['models']['controlnet']
            )
            
            # 加载基础模型
            self._load_base_model()
            
            logger.info("AI引擎初始化完成")
            
        except Exception as e:
            logger.error(f"AI引擎初始化失败: {e}")
            raise
    
    def _load_base_model(self):
        """加载基础Stable Diffusion模型"""
        try:
            model_config = self.config['models']['base_model']
            model_path = model_config['path']
            
            logger.info(f"加载基础模型: {model_path}")
            
            # 加载Stable Diffusion管道
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if self.device.type == 'cuda' else torch.float32,
                safety_checker=None,  # 移除安全检查器
                requires_safety_checker=False
            )
            
            # 移动到指定设备
            self.pipeline = self.pipeline.to(self.device)
            
            # 启用内存优化
            if self.config['hardware']['memory_efficient']:
                self.pipeline.enable_attention_slicing()
                self.pipeline.enable_vae_slicing()
                
            # 启用xformers优化
            if self.config['hardware']['use_xformers'] and hasattr(self.pipeline, 'enable_xformers_memory_efficient_attention'):
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    logger.info("已启用xformers优化")
                except Exception as e:
                    logger.warning(f"xformers优化启用失败: {e}")
            
            logger.info("基础模型加载完成")
            
        except Exception as e:
            logger.error(f"基础模型加载失败: {e}")
            raise
    
    def load_lora(self, lora_name: str) -> bool:
        """
        加载指定的LoRA模型
        
        Args:
            lora_name: LoRA模型名称
            
        Returns:
            bool: 加载是否成功
        """
        try:
            success = self.lora_manager.load_lora(lora_name, self.pipeline)
            if success:
                logger.info(f"LoRA模型 {lora_name} 加载成功")
            return success
        except Exception as e:
            logger.error(f"LoRA模型 {lora_name} 加载失败: {e}")
            return False
    
    def generate_images(
        self,
        prompt: str,
        controlnet_input: Optional[torch.Tensor] = None,
        negative_prompt: str = "",
        num_images: int = 4,
        **kwargs
    ) -> List[torch.Tensor]:
        """
        生成图像
        
        Args:
            prompt: 正面提示词
            controlnet_input: ControlNet输入图像
            negative_prompt: 负面提示词
            num_images: 生成图像数量
            **kwargs: 其他生成参数
            
        Returns:
            List[torch.Tensor]: 生成的图像列表
        """
        try:
            # 获取生成参数
            gen_config = self.config['generation']
            
            # 设置默认参数
            params = {
                'num_inference_steps': gen_config['num_inference_steps'],
                'guidance_scale': gen_config['guidance_scale'],
                'width': gen_config['width'],
                'height': gen_config['height'],
                'num_images_per_prompt': num_images,
                **kwargs
            }
            
            # 处理ControlNet输入
            if controlnet_input is not None:
                # 使用ControlNet进行生成
                result = self.controlnet_processor.generate_with_controlnet(
                    self.pipeline,
                    prompt=prompt,
                    controlnet_input=controlnet_input,
                    negative_prompt=negative_prompt,
                    **params
                )
            else:
                # 标准生成
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    **params
                )
            
            # 提取图像
            images = result.images
            
            logger.info(f"成功生成 {len(images)} 张图像")
            return images
            
        except Exception as e:
            logger.error(f"图像生成失败: {e}")
            raise
    
    def get_available_loras(self) -> List[str]:
        """获取可用的LoRA模型列表"""
        return self.lora_manager.get_available_loras()
    
    def get_lora_info(self, lora_name: str) -> Dict:
        """获取LoRA模型信息"""
        return self.lora_manager.get_lora_info(lora_name)
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.pipeline is not None:
                del self.pipeline
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info("资源清理完成")
        except Exception as e:
            logger.error(f"资源清理失败: {e}")
    
    def __del__(self):
        """析构函数"""
        self.cleanup()
