"""
Streamlit用户界面
提供Web界面进行AI辅助工业设计
"""

import streamlit as st
import numpy as np
from PIL import Image
import logging
from pathlib import Path
import sys
import os

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.image_generator import ImageGenerator
from src.utils.cad_processor import CADProcessor

# 配置页面
st.set_page_config(
    page_title="GAT - AI辅助工业设计",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_session_state():
    """初始化会话状态"""
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'cad_processor' not in st.session_state:
        st.session_state.cad_processor = None
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    if 'generation_params' not in st.session_state:
        st.session_state.generation_params = {}


def load_components():
    """加载组件"""
    try:
        if st.session_state.generator is None:
            with st.spinner("正在初始化AI引擎..."):
                st.session_state.generator = ImageGenerator()
                st.session_state.cad_processor = CADProcessor()
        return True
    except Exception as e:
        st.error(f"组件加载失败: {e}")
        return False


def main():
    """主界面"""
    initialize_session_state()
    
    # 标题
    st.title("🎨 GAT - AI辅助工业设计系统")
    st.markdown("基于Stable Diffusion + LoRA的智能工业设计工具")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # LoRA模型选择
        if st.session_state.generator:
            available_loras = st.session_state.generator.get_available_loras()
            selected_lora = st.selectbox(
                "选择LoRA模型",
                available_loras,
                index=0 if available_loras else None
            )
        else:
            selected_lora = "morphy_richards"
        
        # 生成参数
        st.subheader("生成参数")
        num_images = st.slider("生成图像数量", 1, 8, 4)
        controlnet_method = st.selectbox(
            "ControlNet方法",
            ["canny", "sketch", "depth"],
            index=0
        )
        
        # 高级设置
        with st.expander("高级设置"):
            guidance_scale = st.slider("引导强度", 1.0, 20.0, 7.5)
            num_inference_steps = st.slider("推理步数", 10, 50, 20)
            seed = st.number_input("随机种子", value=-1, help="-1表示随机")
    
    # 主界面布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 输入")
        
        # CAD文件上传
        uploaded_file = st.file_uploader(
            "上传CAD文件",
            type=['png', 'jpg', 'jpeg', 'obj', 'stl', 'ply'],
            help="支持图像文件和3D模型文件"
        )
        
        # 或者使用示例图像
        if st.button("使用示例图像"):
            # 创建一个示例图像
            example_image = np.ones((512, 512, 3), dtype=np.uint8) * 255
            st.session_state.example_image = example_image
            st.success("已加载示例图像")
        
        # 显示输入图像
        if uploaded_file is not None:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="输入图像", use_column_width=True)
        elif 'example_image' in st.session_state:
            st.image(st.session_state.example_image, caption="示例图像", use_column_width=True)
        
        # 提示词输入
        st.subheader("💭 提示词")
        base_prompt = st.text_area(
            "描述您想要的产品",
            value="home appliance, modern design, white color, minimalist style",
            height=100,
            help="描述产品的特征、风格、颜色等"
        )
        
        # 负面提示词
        negative_prompt = st.text_input(
            "负面提示词",
            value="blurry, low quality, distorted, ugly",
            help="描述不想要的特征"
        )
    
    with col2:
        st.header("🎯 生成")
        
        # 生成按钮
        if st.button("🚀 开始生成", type="primary"):
            if not load_components():
                st.stop()
            
            # 检查输入
            if uploaded_file is None and 'example_image' not in st.session_state:
                st.warning("请先上传CAD文件或使用示例图像")
                st.stop()
            
            if not base_prompt.strip():
                st.warning("请输入提示词")
                st.stop()
            
            # 准备输入
            if uploaded_file is not None:
                input_data = Image.open(uploaded_file)
            else:
                input_data = st.session_state.example_image
            
            # 生成参数
            generation_params = {
                'guidance_scale': guidance_scale,
                'num_inference_steps': num_inference_steps,
                'negative_prompt': negative_prompt
            }
            
            if seed != -1:
                generation_params['seed'] = seed
            
            # 执行生成
            with st.spinner("正在生成图像..."):
                try:
                    result = st.session_state.generator.generate_from_cad(
                        cad_input=input_data,
                        prompt=base_prompt,
                        lora_name=selected_lora,
                        controlnet_method=controlnet_method,
                        num_images=num_images,
                        **generation_params
                    )
                    
                    st.session_state.generated_images = result['images']
                    st.session_state.generation_params = result
                    
                    st.success(f"成功生成 {len(result['images'])} 张图像！")
                    
                except Exception as e:
                    st.error(f"生成失败: {e}")
                    logger.error(f"生成失败: {e}")
        
        # 显示生成结果
        if st.session_state.generated_images:
            st.subheader("🖼️ 生成结果")
            
            # 显示图像网格
            cols = st.columns(2)
            for i, image in enumerate(st.session_state.generated_images):
                with cols[i % 2]:
                    st.image(image, caption=f"生成图像 {i+1}", use_column_width=True)
            
            # 下载按钮
            st.subheader("💾 下载")
            for i, image in enumerate(st.session_state.generated_images):
                st.download_button(
                    label=f"下载图像 {i+1}",
                    data=image_to_bytes(image),
                    file_name=f"generated_{i+1}.png",
                    mime="image/png"
                )
    
    # 底部信息
    st.markdown("---")
    st.markdown("### 📊 系统信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("可用LoRA模型", len(available_loras) if st.session_state.generator else 0)
    
    with col2:
        st.metric("生成图像数量", len(st.session_state.generated_images))
    
    with col3:
        if st.session_state.generation_params:
            st.metric("使用模型", st.session_state.generation_params.get('lora_used', 'N/A'))


def image_to_bytes(image: Image.Image) -> bytes:
    """将PIL图像转换为字节"""
    import io
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()


if __name__ == "__main__":
    main()
