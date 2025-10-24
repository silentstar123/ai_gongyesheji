"""
LoRA模型管理器
负责LoRA模型的加载、管理和应用
"""

import torch
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class LoRAManager:
    """LoRA模型管理器"""
    
    def __init__(self, lora_config: Dict):
        """
        初始化LoRA管理器
        
        Args:
            lora_config: LoRA配置字典
        """
        self.config = lora_config
        self.loaded_loras = {}
        self.available_loras = self._scan_available_loras()
        
    def _scan_available_loras(self) -> Dict[str, Dict]:
        """扫描可用的LoRA模型"""
        available = {}
        
        for lora_name, lora_info in self.config.items():
            if isinstance(lora_info, dict) and lora_info.get('enabled', True):
                lora_path = Path(lora_info['path'])
                if lora_path.exists():
                    available[lora_name] = {
                        'path': str(lora_path),
                        'trigger_word': lora_info.get('trigger_word', ''),
                        'weight': lora_info.get('weight', 0.8),
                        'enabled': lora_info.get('enabled', True)
                    }
                else:
                    logger.warning(f"LoRA模型文件不存在: {lora_path}")
        
        return available
    
    def load_lora(self, lora_name: str, pipeline: Any) -> bool:
        """
        加载LoRA模型到管道
        
        Args:
            lora_name: LoRA模型名称
            pipeline: Stable Diffusion管道
            
        Returns:
            bool: 加载是否成功
        """
        try:
            if lora_name not in self.available_loras:
                logger.error(f"LoRA模型 {lora_name} 不可用")
                return False
            
            lora_info = self.available_loras[lora_name]
            lora_path = lora_info['path']
            weight = lora_info['weight']
            
            logger.info(f"加载LoRA模型: {lora_name} (权重: {weight})")
            
            # 加载LoRA权重
            if lora_path.endswith('.safetensors'):
                lora_state_dict = self._load_safetensors(lora_path)
            else:
                lora_state_dict = torch.load(lora_path, map_location='cpu')
            
            # 应用LoRA权重到管道
            self._apply_lora_to_pipeline(pipeline, lora_state_dict, weight)
            
            # 记录已加载的LoRA
            self.loaded_loras[lora_name] = {
                'weight': weight,
                'trigger_word': lora_info['trigger_word']
            }
            
            logger.info(f"LoRA模型 {lora_name} 加载成功")
            return True
            
        except Exception as e:
            logger.error(f"LoRA模型 {lora_name} 加载失败: {e}")
            return False
    
    def _load_safetensors(self, file_path: str) -> Dict[str, torch.Tensor]:
        """加载SafeTensors格式的LoRA文件"""
        from safetensors import safe_open
        
        state_dict = {}
        with safe_open(file_path, framework="pt", device="cpu") as f:
            for key in f.keys():
                state_dict[key] = f.get_tensor(key)
        
        return state_dict
    
    def _apply_lora_to_pipeline(self, pipeline: Any, lora_state_dict: Dict, weight: float):
        """将LoRA权重应用到管道"""
        try:
            # 获取unet和text_encoder
            unet = pipeline.unet
            text_encoder = pipeline.text_encoder
            
            # 应用LoRA权重到UNet
            self._apply_lora_to_unet(unet, lora_state_dict, weight)
            
            # 应用LoRA权重到Text Encoder（如果存在）
            self._apply_lora_to_text_encoder(text_encoder, lora_state_dict, weight)
            
        except Exception as e:
            logger.error(f"应用LoRA权重失败: {e}")
            raise
    
    def _apply_lora_to_unet(self, unet: Any, lora_state_dict: Dict, weight: float):
        """将LoRA权重应用到UNet"""
        for name, module in unet.named_modules():
            if 'lora' in name.lower():
                # 查找对应的LoRA权重
                lora_key = name.replace('.', '_')
                if lora_key in lora_state_dict:
                    # 应用LoRA权重
                    lora_weight = lora_state_dict[lora_key] * weight
                    if hasattr(module, 'weight'):
                        module.weight.data += lora_weight
    
    def _apply_lora_to_text_encoder(self, text_encoder: Any, lora_state_dict: Dict, weight: float):
        """将LoRA权重应用到Text Encoder"""
        for name, module in text_encoder.named_modules():
            if 'lora' in name.lower():
                lora_key = name.replace('.', '_')
                if lora_key in lora_state_dict:
                    lora_weight = lora_state_dict[lora_key] * weight
                    if hasattr(module, 'weight'):
                        module.weight.data += lora_weight
    
    def unload_lora(self, lora_name: str) -> bool:
        """
        卸载LoRA模型
        
        Args:
            lora_name: LoRA模型名称
            
        Returns:
            bool: 卸载是否成功
        """
        try:
            if lora_name in self.loaded_loras:
                del self.loaded_loras[lora_name]
                logger.info(f"LoRA模型 {lora_name} 已卸载")
                return True
            else:
                logger.warning(f"LoRA模型 {lora_name} 未加载")
                return False
        except Exception as e:
            logger.error(f"卸载LoRA模型 {lora_name} 失败: {e}")
            return False
    
    def get_available_loras(self) -> List[str]:
        """获取可用的LoRA模型列表"""
        return list(self.available_loras.keys())
    
    def get_loaded_loras(self) -> List[str]:
        """获取已加载的LoRA模型列表"""
        return list(self.loaded_loras.keys())
    
    def get_lora_info(self, lora_name: str) -> Optional[Dict]:
        """获取LoRA模型信息"""
        if lora_name in self.available_loras:
            return self.available_loras[lora_name]
        return None
    
    def is_lora_loaded(self, lora_name: str) -> bool:
        """检查LoRA模型是否已加载"""
        return lora_name in self.loaded_loras
    
    def get_trigger_words(self) -> List[str]:
        """获取所有已加载LoRA的触发词"""
        trigger_words = []
        for lora_info in self.loaded_loras.values():
            if lora_info['trigger_word']:
                trigger_words.append(lora_info['trigger_word'])
        return trigger_words
    
    def create_prompt_with_loras(self, base_prompt: str) -> str:
        """
        创建包含LoRA触发词的提示词
        
        Args:
            base_prompt: 基础提示词
            
        Returns:
            str: 包含LoRA触发词的完整提示词
        """
        trigger_words = self.get_trigger_words()
        if trigger_words:
            lora_prompt = ", ".join(trigger_words)
            return f"{lora_prompt}, {base_prompt}"
        return base_prompt
