"""
ControlNet处理器
负责处理ControlNet输入和生成控制
"""

import torch
import cv2
import numpy as np
from typing import Optional, Union, Tuple
import logging
from PIL import Image

from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from controlnet_aux import CannyDetector, OpenposeDetector, MidasDetector

logger = logging.getLogger(__name__)


class ControlNetProcessor:
    """ControlNet处理器"""
    
    def __init__(self, controlnet_config: dict):
        """
        初始化ControlNet处理器
        
        Args:
            controlnet_config: ControlNet配置
        """
        self.config = controlnet_config
        self.controlnet_models = {}
        self.detectors = {}
        self.pipeline = None
        
        # 初始化检测器
        self._initialize_detectors()
        
    def _initialize_detectors(self):
        """初始化各种检测器"""
        try:
            # Canny边缘检测器
            self.detectors['canny'] = CannyDetector()
            
            # OpenPose姿态检测器
            self.detectors['openpose'] = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
            
            # Midas深度检测器
            self.detectors['midas'] = MidasDetector.from_pretrained("lllyasviel/ControlNet")
            
            logger.info("ControlNet检测器初始化完成")
            
        except Exception as e:
            logger.error(f"ControlNet检测器初始化失败: {e}")
            raise
    
    def load_controlnet_model(self, controlnet_type: str, device: torch.device) -> bool:
        """
        加载ControlNet模型
        
        Args:
            controlnet_type: ControlNet类型 (sketch, canny, depth)
            device: 计算设备
            
        Returns:
            bool: 加载是否成功
        """
        try:
            if controlnet_type not in self.config['models']:
                logger.error(f"不支持的ControlNet类型: {controlnet_type}")
                return False
            
            model_path = self.config['models'][controlnet_type]
            
            logger.info(f"加载ControlNet模型: {controlnet_type}")
            
            # 加载ControlNet模型
            controlnet = ControlNetModel.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if device.type == 'cuda' else torch.float32
            )
            
            self.controlnet_models[controlnet_type] = controlnet.to(device)
            
            logger.info(f"ControlNet模型 {controlnet_type} 加载成功")
            return True
            
        except Exception as e:
            logger.error(f"ControlNet模型 {controlnet_type} 加载失败: {e}")
            return False
    
    def create_controlnet_pipeline(self, base_pipeline, controlnet_type: str) -> bool:
        """
        创建ControlNet管道
        
        Args:
            base_pipeline: 基础Stable Diffusion管道
            controlnet_type: ControlNet类型
            
        Returns:
            bool: 创建是否成功
        """
        try:
            if controlnet_type not in self.controlnet_models:
                logger.error(f"ControlNet模型 {controlnet_type} 未加载")
                return False
            
            controlnet = self.controlnet_models[controlnet_type]
            
            # 创建ControlNet管道
            self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
                base_pipeline,
                controlnet=controlnet,
                torch_dtype=torch.float16 if controlnet.device.type == 'cuda' else torch.float32
            )
            
            # 启用优化
            if hasattr(self.pipeline, 'enable_attention_slicing'):
                self.pipeline.enable_attention_slicing()
            
            logger.info(f"ControlNet管道 {controlnet_type} 创建成功")
            return True
            
        except Exception as e:
            logger.error(f"ControlNet管道创建失败: {e}")
            return False
    
    def process_cad_input(self, cad_image: Union[str, np.ndarray, Image.Image], 
                         method: str = "canny") -> np.ndarray:
        """
        处理CAD输入图像
        
        Args:
            cad_image: CAD图像（路径、numpy数组或PIL图像）
            method: 处理方法 (canny, sketch, depth)
            
        Returns:
            np.ndarray: 处理后的控制图像
        """
        try:
            # 加载图像
            if isinstance(cad_image, str):
                image = cv2.imread(cad_image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif isinstance(cad_image, np.ndarray):
                image = cad_image
            elif isinstance(cad_image, Image.Image):
                image = np.array(cad_image)
            else:
                raise ValueError("不支持的图像格式")
            
            # 根据方法处理图像
            if method == "canny":
                return self._process_canny(image)
            elif method == "sketch":
                return self._process_sketch(image)
            elif method == "depth":
                return self._process_depth(image)
            else:
                raise ValueError(f"不支持的处理方法: {method}")
                
        except Exception as e:
            logger.error(f"CAD输入处理失败: {e}")
            raise
    
    def _process_canny(self, image: np.ndarray) -> np.ndarray:
        """Canny边缘检测处理"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Canny边缘检测
            canny = cv2.Canny(gray, 100, 200)
            
            # 转换为3通道
            canny_3ch = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
            
            return canny_3ch
            
        except Exception as e:
            logger.error(f"Canny处理失败: {e}")
            raise
    
    def _process_sketch(self, image: np.ndarray) -> np.ndarray:
        """素描风格处理"""
        try:
            # 转换为灰度图
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # 计算梯度
            grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
            
            # 计算梯度幅值
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # 归一化
            sketch = (gradient_magnitude * 255).astype(np.uint8)
            
            # 转换为3通道
            sketch_3ch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
            
            return sketch_3ch
            
        except Exception as e:
            logger.error(f"Sketch处理失败: {e}")
            raise
    
    def _process_depth(self, image: np.ndarray) -> np.ndarray:
        """深度图处理"""
        try:
            # 使用Midas检测器
            if 'midas' in self.detectors:
                depth = self.detectors['midas'](image)
                return depth
            else:
                # 简单的深度估计
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
                depth = cv2.Laplacian(gray, cv2.CV_64F)
                depth = np.abs(depth)
                depth = (depth / depth.max() * 255).astype(np.uint8)
                return cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
                
        except Exception as e:
            logger.error(f"Depth处理失败: {e}")
            raise
    
    def generate_with_controlnet(self, pipeline, prompt: str, controlnet_input: torch.Tensor,
                                negative_prompt: str = "", **kwargs) -> dict:
        """
        使用ControlNet生成图像
        
        Args:
            pipeline: ControlNet管道
            prompt: 提示词
            controlnet_input: ControlNet输入
            negative_prompt: 负面提示词
            **kwargs: 其他生成参数
            
        Returns:
            dict: 生成结果
        """
        try:
            if self.pipeline is None:
                raise ValueError("ControlNet管道未初始化")
            
            # 生成参数
            generation_params = {
                'prompt': prompt,
                'image': controlnet_input,
                'negative_prompt': negative_prompt,
                'num_inference_steps': kwargs.get('num_inference_steps', 20),
                'guidance_scale': kwargs.get('guidance_scale', 7.5),
                'controlnet_conditioning_scale': kwargs.get('controlnet_conditioning_scale', 1.0),
                'num_images_per_prompt': kwargs.get('num_images_per_prompt', 1)
            }
            
            # 生成图像
            result = self.pipeline(**generation_params)
            
            logger.info("ControlNet图像生成完成")
            return result
            
        except Exception as e:
            logger.error(f"ControlNet生成失败: {e}")
            raise
    
    def extract_six_views(self, cad_model_path: str) -> dict:
        """
        从CAD模型提取六视图
        
        Args:
            cad_model_path: CAD模型文件路径
            
        Returns:
            dict: 六视图图像字典
        """
        try:
            # 这里需要集成CAD处理库（如FreeCAD, OpenCASCADE等）
            # 暂时返回占位符
            views = {
                'front': None,
                'back': None,
                'left': None,
                'right': None,
                'top': None,
                'bottom': None
            }
            
            logger.info("六视图提取功能待实现")
            return views
            
        except Exception as e:
            logger.error(f"六视图提取失败: {e}")
            raise
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.pipeline is not None:
                del self.pipeline
            self.controlnet_models.clear()
            self.detectors.clear()
            logger.info("ControlNet处理器资源清理完成")
        except Exception as e:
            logger.error(f"ControlNet处理器资源清理失败: {e}")
