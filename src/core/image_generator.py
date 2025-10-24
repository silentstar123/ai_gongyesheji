"""
图像生成器
负责协调AI引擎、LoRA和ControlNet进行图像生成
"""

import torch
import logging
from typing import List, Dict, Optional, Union, Tuple
from PIL import Image
import numpy as np
from pathlib import Path

from .ai_engine import AIEngine
from .lora_manager import LoRAManager
from .controlnet_processor import ControlNetProcessor

logger = logging.getLogger(__name__)


class ImageGenerator:
    """图像生成器主类"""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """
        初始化图像生成器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.ai_engine = None
        self.generation_config = None
        
        # 初始化组件
        self._initialize()
    
    def _initialize(self):
        """初始化所有组件"""
        try:
            # 初始化AI引擎
            self.ai_engine = AIEngine(self.config_path)
            
            # 获取生成配置
            import yaml
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.generation_config = config['generation']
            
            logger.info("图像生成器初始化完成")
            
        except Exception as e:
            logger.error(f"图像生成器初始化失败: {e}")
            raise
    
    def generate_from_cad(
        self,
        cad_input: Union[str, np.ndarray, Image.Image],
        prompt: str,
        lora_name: str = "morphy_richards",
        controlnet_method: str = "canny",
        num_images: int = 4,
        **kwargs
    ) -> Dict[str, any]:
        """
        从CAD输入生成图像
        
        Args:
            cad_input: CAD输入（文件路径、numpy数组或PIL图像）
            prompt: 生成提示词
            lora_name: 使用的LoRA模型名称
            controlnet_method: ControlNet处理方法
            num_images: 生成图像数量
            **kwargs: 其他生成参数
            
        Returns:
            Dict: 生成结果字典
        """
        try:
            logger.info(f"开始从CAD生成图像，LoRA: {lora_name}, 方法: {controlnet_method}")
            
            # 1. 加载LoRA模型
            if not self.ai_engine.load_lora(lora_name):
                raise ValueError(f"LoRA模型 {lora_name} 加载失败")
            
            # 2. 处理CAD输入
            controlnet_input = self._process_cad_input(cad_input, controlnet_method)
            
            # 3. 构建完整提示词
            full_prompt = self._build_prompt(prompt, lora_name)
            
            # 4. 生成图像
            images = self.ai_engine.generate_images(
                prompt=full_prompt,
                controlnet_input=controlnet_input,
                num_images=num_images,
                **kwargs
            )
            
            # 5. 后处理图像
            processed_images = self._post_process_images(images)
            
            # 6. 构建结果
            result = {
                'images': processed_images,
                'prompt': full_prompt,
                'lora_used': lora_name,
                'controlnet_method': controlnet_method,
                'num_generated': len(processed_images),
                'generation_params': kwargs
            }
            
            logger.info(f"成功生成 {len(processed_images)} 张图像")
            return result
            
        except Exception as e:
            logger.error(f"CAD图像生成失败: {e}")
            raise
    
    def generate_batch(
        self,
        cad_inputs: List[Union[str, np.ndarray, Image.Image]],
        prompts: List[str],
        lora_name: str = "morphy_richards",
        controlnet_method: str = "canny",
        **kwargs
    ) -> List[Dict[str, any]]:
        """
        批量生成图像
        
        Args:
            cad_inputs: CAD输入列表
            prompts: 提示词列表
            lora_name: 使用的LoRA模型名称
            controlnet_method: ControlNet处理方法
            **kwargs: 其他生成参数
            
        Returns:
            List[Dict]: 批量生成结果列表
        """
        try:
            results = []
            
            for i, (cad_input, prompt) in enumerate(zip(cad_inputs, prompts)):
                logger.info(f"处理第 {i+1}/{len(cad_inputs)} 个输入")
                
                result = self.generate_from_cad(
                    cad_input=cad_input,
                    prompt=prompt,
                    lora_name=lora_name,
                    controlnet_method=controlnet_method,
                    **kwargs
                )
                
                results.append(result)
            
            logger.info(f"批量生成完成，共处理 {len(results)} 个输入")
            return results
            
        except Exception as e:
            logger.error(f"批量生成失败: {e}")
            raise
    
    def _process_cad_input(self, cad_input: Union[str, np.ndarray, Image.Image], 
                          method: str) -> torch.Tensor:
        """处理CAD输入"""
        try:
            # 使用ControlNet处理器处理CAD输入
            processed_image = self.ai_engine.controlnet_processor.process_cad_input(
                cad_input, method
            )
            
            # 转换为tensor
            if isinstance(processed_image, np.ndarray):
                # 归一化到[0, 1]
                processed_image = processed_image.astype(np.float32) / 255.0
                
                # 转换为tensor
                tensor = torch.from_numpy(processed_image).permute(2, 0, 1).unsqueeze(0)
                
                # 移动到设备
                tensor = tensor.to(self.ai_engine.device)
                
                return tensor
            else:
                raise ValueError("CAD输入处理失败")
                
        except Exception as e:
            logger.error(f"CAD输入处理失败: {e}")
            raise
    
    def _build_prompt(self, base_prompt: str, lora_name: str) -> str:
        """构建完整提示词"""
        try:
            # 获取LoRA触发词
            lora_info = self.ai_engine.lora_manager.get_lora_info(lora_name)
            if lora_info and lora_info.get('trigger_word'):
                trigger_word = lora_info['trigger_word']
                full_prompt = f"{trigger_word}, {base_prompt}"
            else:
                full_prompt = base_prompt
            
            # 添加质量提升词
            quality_terms = [
                "high quality", "detailed", "professional", "industrial design",
                "realistic", "sharp focus", "well lit", "studio lighting"
            ]
            
            enhanced_prompt = f"{full_prompt}, {', '.join(quality_terms)}"
            
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"提示词构建失败: {e}")
            return base_prompt
    
    def _post_process_images(self, images: List[torch.Tensor]) -> List[Image.Image]:
        """后处理生成的图像"""
        try:
            processed_images = []
            
            for i, image_tensor in enumerate(images):
                # 转换为PIL图像
                if isinstance(image_tensor, torch.Tensor):
                    # 确保在CPU上
                    image_tensor = image_tensor.cpu()
                    
                    # 转换为numpy数组
                    if image_tensor.dim() == 4:
                        image_tensor = image_tensor.squeeze(0)
                    
                    # 重新排列维度 (C, H, W) -> (H, W, C)
                    image_array = image_tensor.permute(1, 2, 0).numpy()
                    
                    # 确保值在[0, 1]范围内
                    image_array = np.clip(image_array, 0, 1)
                    
                    # 转换为0-255范围
                    image_array = (image_array * 255).astype(np.uint8)
                    
                    # 创建PIL图像
                    pil_image = Image.fromarray(image_array)
                    
                elif isinstance(image_tensor, Image.Image):
                    pil_image = image_tensor
                else:
                    raise ValueError(f"不支持的图像类型: {type(image_tensor)}")
                
                processed_images.append(pil_image)
            
            return processed_images
            
        except Exception as e:
            logger.error(f"图像后处理失败: {e}")
            raise
    
    def save_images(self, images: List[Image.Image], output_dir: str, 
                   prefix: str = "generated") -> List[str]:
        """
        保存生成的图像
        
        Args:
            images: 图像列表
            output_dir: 输出目录
            prefix: 文件名前缀
            
        Returns:
            List[str]: 保存的文件路径列表
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            saved_paths = []
            
            for i, image in enumerate(images):
                filename = f"{prefix}_{i+1:03d}.png"
                filepath = output_path / filename
                
                image.save(filepath, "PNG", quality=95)
                saved_paths.append(str(filepath))
                
                logger.info(f"图像已保存: {filepath}")
            
            return saved_paths
            
        except Exception as e:
            logger.error(f"图像保存失败: {e}")
            raise
    
    def get_available_loras(self) -> List[str]:
        """获取可用的LoRA模型列表"""
        return self.ai_engine.get_available_loras()
    
    def get_generation_config(self) -> Dict:
        """获取生成配置"""
        return self.generation_config
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.ai_engine:
                self.ai_engine.cleanup()
            logger.info("图像生成器资源清理完成")
        except Exception as e:
            logger.error(f"图像生成器资源清理失败: {e}")
    
    def __del__(self):
        """析构函数"""
        self.cleanup()
