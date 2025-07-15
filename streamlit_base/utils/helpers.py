"""도우미 함수들"""
import base64
import io
from pathlib import Path
from PIL import Image
import streamlit as st
from typing import List, Optional, Tuple

def get_base64_image(image_path: Path, max_size: Optional[Tuple[int, int]] = None) -> str:
    """이미지를 base64로 인코딩"""
    try:
        with open(image_path, "rb") as img_file:
            img = Image.open(img_file)
            
            # 크기 조정
            if max_size:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # PNG로 변환
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
    
    except Exception as e:
        st.error(f"이미지 인코딩 오류: {str(e)}")
        return ""

def get_gallery_images(gallery_path: Path) -> List[Path]:
    """갤러리 디렉토리에서 이미지 파일들 가져오기"""
    if not gallery_path.exists():
        return []
    
    supported_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    images = []
    
    for ext in supported_extensions:
        images.extend(gallery_path.glob(f"*{ext}"))
        images.extend(gallery_path.glob(f"*{ext.upper()}"))
    
    return sorted(images)

def validate_image_file(uploaded_file) -> Optional[Image.Image]:
    """업로드된 파일 검증 및 이미지 로드"""
    if not uploaded_file:
        return None
    
    try:
        # 파일 크기 검증
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.error("파일 크기가 너무 큽니다. 10MB 이하의 파일을 업로드해주세요.")
            return None
        
        # 이미지 로드
        image = Image.open(uploaded_file)
        
        # 이미지 크기 검증
        if image.size[0] > 4096 or image.size[1] > 4096:
            st.warning("이미지가 너무 큽니다. 크기를 조정합니다.")
            image.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
        
        return image.convert("RGBA")
    
    except Exception as e:
        st.error(f"이미지 파일을 읽을 수 없습니다: {str(e)}")
        return None

def format_file_size(size_bytes: int) -> str:
    """바이트를 읽기 쉬운 형식으로 변환"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def create_thumbnail(image: Image.Image, size: Tuple[int, int] = (200, 200)) -> Image.Image:
    """썸네일 이미지 생성"""
    thumbnail = image.copy()
    thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
    return thumbnail

def safe_filename(filename: str) -> str:
    """안전한 파일명으로 변환"""
    import re
    # 특수문자 제거
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 연속된 밑줄 제거
    safe_name = re.sub(r'_+', '_', safe_name)
    # 앞뒤 공백 및 밑줄 제거
    safe_name = safe_name.strip(' _')
    
    return safe_name or "unnamed"

def calculate_aspect_ratio(width: int, height: int) -> str:
    """가로세로 비율 계산"""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    ratio_gcd = gcd(width, height)
    ratio_w = width // ratio_gcd
    ratio_h = height // ratio_gcd
    
    return f"{ratio_w}:{ratio_h}"

def resize_image_to_target(image: Image.Image, target_width: int, target_height: int, 
                          maintain_aspect: bool = True) -> Image.Image:
    """이미지를 목표 크기로 리사이즈"""
    if maintain_aspect:
        image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # 캔버스 생성하여 중앙 배치
        canvas = Image.new('RGBA', (target_width, target_height), (255, 255, 255, 0))
        x = (target_width - image.width) // 2
        y = (target_height - image.height) // 2
        canvas.paste(image, (x, y), image if image.mode == 'RGBA' else None)
        
        return canvas
    else:
        return image.resize((target_width, target_height), Image.Resampling.LANCZOS)

@st.cache_data(ttl=3600)
def get_font_preview(font_name: str, text: str = "미리보기") -> str:
    """폰트 미리보기 HTML 생성"""
    return f"""
    <div style="
        font-family: '{font_name}', sans-serif;
        font-size: 24px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        text-align: center;
        margin: 5px 0;
    ">
        {text}
    </div>
    """

def show_progress_bar(progress: float, message: str = ""):
    """진행률 표시"""
    progress_bar = st.progress(progress)
    if message:
        st.text(message)
    return progress_bar

def display_image_info(image: Image.Image):
    """이미지 정보 표시"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("크기", f"{image.size[0]} × {image.size[1]}")
    
    with col2:
        st.metric("비율", calculate_aspect_ratio(image.size[0], image.size[1]))
    
    with col3:
        st.metric("모드", image.mode)