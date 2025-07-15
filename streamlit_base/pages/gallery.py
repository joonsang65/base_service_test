"""갤러리 페이지"""
import streamlit as st
from pathlib import Path
from core.config import config
from utils.styles import GALLERY_CSS
from utils.helpers import get_gallery_images

def render():
    """갤러리 페이지 렌더링"""
    st.markdown(GALLERY_CSS, unsafe_allow_html=True)
    
    st.title("🖼️ 광고 갤러리")
    st.markdown("### AI로 제작된 다양한 광고 예시들을 확인해보세요!")
    
    # 플랫폼별 갤러리
    tab1, tab2, tab3 = st.tabs(["📸 인스타그램", "📝 블로그", "🖼️ 포스터"])
    
    with tab1:
        render_platform_gallery("인스타그램", "instagram")
    
    with tab2:
        render_platform_gallery("블로그", "blog")
    
    with tab3:
        render_platform_gallery("포스터", "poster")
    
    # 슬라이딩 갤러리
    st.markdown("---")
    st.markdown("## 🎞️ 전체 갤러리")
    render_sliding_gallery()

def render_platform_gallery(platform_name, platform_key):
    """플랫폼별 갤러리 렌더링"""
    st.markdown(f"### {platform_name} 광고 모음")
    
    gallery_path = config.get_image_path() / "gallery" / platform_key
    images = get_gallery_images(gallery_path)
    
    if not images:
        st.info(f"아직 {platform_name} 갤러리에 이미지가 없습니다. 곧 업데이트될 예정입니다!")
        return
    
    # 그리드 형태로 이미지 표시
    cols = st.columns(3)
    
    for i, image_path in enumerate(images):
        with cols[i % 3]:
            st.image(str(image_path), use_container_width=True)
            
            # 이미지 정보
            image_name = image_path.stem
            st.caption(f"📅 {image_name}")
            
            # 다운로드 버튼
            with open(image_path, "rb") as file:
                st.download_button(
                    label="📥 다운로드",
                    data=file.read(),
                    file_name=image_path.name,
                    mime="image/png",
                    key=f"download_{platform_key}_{i}"
                )

def render_sliding_gallery():
    """슬라이딩 갤러리 렌더링"""
    # 모든 갤러리 이미지 수집
    all_images = []
    gallery_base = config.get_image_path() / "gallery"
    
    for platform_dir in ["instagram", "blog", "poster"]:
        platform_path = gallery_base / platform_dir
        if platform_path.exists():
            all_images.extend(get_gallery_images(platform_path))
    
    if not all_images:
        st.info("갤러리 이미지가 준비 중입니다. 곧 업데이트될 예정입니다!")
        return
    
    # 이미지들을 base64로 변환
    from utils.helpers import get_base64_image
    encoded_images = []
    
    for img_path in all_images[:12]:  # 최대 12개만 표시
        try:
            encoded_img = get_base64_image(img_path)
            encoded_images.append(encoded_img)
        except Exception:
            continue
    
    if not encoded_images:
        st.info("이미지를 로드할 수 없습니다.")
        return
    
    # 3줄 슬라이더 생성
    directions = ["scroll-left", "scroll-right", "scroll-left"]
    durations = [50, 60, 70]
    
    # 이미지를 3그룹으로 분할
    chunks = [encoded_images[i::3] for i in range(3)]
    
    for i, (images_chunk, direction, duration) in enumerate(zip(chunks, directions, durations)):
        if images_chunk:
            slider_html = create_slider_html(images_chunk, direction, duration)
            st.components.v1.html(slider_html, height=200)

def create_slider_html(images, direction, duration):
    """슬라이더 HTML 생성"""
    # 무한 스크롤을 위해 이미지 2배 복제
    image_tags = "".join([f'<img src="{img}" alt="gallery"/>' for img in images * 2])
    
    slider_class = "slider-right" if direction == "scroll-right" else ""
    
    html = f"""
    <div class="gallery-slider {slider_class}">
        <div class="slide-track" style="animation-duration: {duration}s;">
            {image_tags}
        </div>
    </div>
    """
    
    return html