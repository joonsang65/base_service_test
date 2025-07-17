"""1단계: 제품 이미지 설정"""
import streamlit as st
from PIL import Image
from pathlib import Path
from io import BytesIO
from streamlit_drawable_canvas import st_canvas

from core.session_manager import SessionManager
from core.config import config
from services.api_client import get_api_client
from utils.styles import WORKFLOW_CSS
from components.ui.navigation import render_step_navigation

def render():
    """1단계 메인 렌더링 함수"""
    st.markdown(f"<style>{WORKFLOW_CSS}</style>", unsafe_allow_html=True)
    
    api_client = get_api_client()
    
    # 헤더
    st.markdown("""
    <style>
    <div class="step-header">
        <h2>1️⃣ 제품 이미지 설정 및 배치</h2>
        <p>제품 이미지를 업로드하고 위치를 조정해주세요</p>
    </div>
    </style>
    """, unsafe_allow_html=True)
    
    # 메인 컨텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_image_input_section(api_client)
    
    with col2:
        render_image_positioning_section(api_client)
    
    # 네비게이션
    render_step_navigation(
        current_step=1,
        can_proceed=SessionManager.can_proceed_to_step(2),
        proceed_message="제품 이미지를 먼저 배치해주세요."
    )

def render_image_input_section(api_client):
    """이미지 입력 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("📤 제품 이미지 입력")
    
    # 업로드 모드 선택
    upload_mode = st.radio(
        "입력 방식 선택",
        ["직접 업로드", "AI 생성 (예시)"],
        horizontal=True,
        key="upload_mode_radio"
    )
    
    # 모드 변경 감지
    if upload_mode != SessionManager.get("upload_mode"):
        SessionManager.update({
            "upload_mode": upload_mode,
            "original_image": None,
            "bg_removed_image": None,
            "positioned_image": None,
            "mask_image": None
        })
    
    st.markdown("---")
    
    if upload_mode == "직접 업로드":
        render_file_upload(api_client)
    else:
        render_ai_generation(api_client)
    
    # 결과 이미지 표시
    render_processed_images()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_file_upload(api_client):
    """파일 업로드 UI"""
    uploaded_file = st.file_uploader(
        "제품 이미지를 업로드하세요",
        type=config.ALLOWED_IMAGE_TYPES,
        help=f"지원 형식: {', '.join(config.ALLOWED_IMAGE_TYPES).upper()}"
    )
    
    if uploaded_file:
        try:
            # 이미지 로드
            image = Image.open(uploaded_file).convert("RGBA")
            SessionManager.set("original_image", image)
            
            # 자동 배경 제거
            if not SessionManager.get("bg_removed_image"):
                with st.spinner("🤖 AI가 배경을 제거하고 있습니다..."):
                    original, bg_removed = api_client.remove_background(image)
                    
                    if bg_removed:
                        SessionManager.set("bg_removed_image", bg_removed)
                        st.success("✅ 배경이 성공적으로 제거되었습니다!")
                    else:
                        st.error("❌ 배경 제거에 실패했습니다. 다시 시도해주세요.")
        
        except Exception as e:
            st.error(f"이미지 처리 중 오류가 발생했습니다: {str(e)}")

def render_ai_generation(api_client):
    """AI 생성 UI"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("💡 AI로 제품 이미지를 생성할 수 있습니다 (현재는 예시 이미지 사용)")
        
        product_description = st.text_input(
            "제품 설명",
            placeholder="예: 빨간 사과, 흰색 배경",
            help="생성하고 싶은 제품을 설명해주세요"
        )
    
    with col2:
        if st.button("🎨 이미지 생성", type="primary"):
            if product_description:
                with st.spinner("🤖 AI가 제품 이미지를 생성하고 있습니다..."):
                    # 현재는 예시 이미지 사용 (실제로는 AI 생성 API 호출)
                    example_path = config.get_image_path() / "examples" / "sample_product.png"
                    if example_path.exists():
                        image = Image.open(example_path).convert("RGBA")
                        SessionManager.set("original_image", image)
                        
                        # 배경 제거
                        original, bg_removed = api_client.remove_background(image)
                        if bg_removed:
                            SessionManager.set("bg_removed_image", bg_removed)
                            st.success("✅ AI 제품 이미지가 생성되었습니다!")
                        else:
                            st.error("❌ 배경 제거에 실패했습니다.")
                    else:
                        st.error("❌ 예시 이미지를 찾을 수 없습니다.")
            else:
                st.warning("제품 설명을 입력해주세요.")

def render_processed_images():
    """처리된 이미지들 표시"""
    original = SessionManager.get("original_image")
    bg_removed = SessionManager.get("bg_removed_image")
    
    if original or bg_removed:
        st.markdown("#### 📸 처리 결과")
        
        if original and bg_removed:
            col1, col2 = st.columns(2)
            with col1:
                st.image(original, caption="원본 이미지", use_container_width=True)
            with col2:
                st.image(bg_removed, caption="배경 제거됨", use_container_width=True)
        elif original:
            st.image(original, caption="업로드된 이미지", use_container_width=True)

def render_image_positioning_section(api_client):
    """이미지 배치 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("🎯 제품 배치 조정")
    
    bg_removed = SessionManager.get("bg_removed_image")
    
    if not bg_removed:
        st.markdown("""
        <div class="image-preview">
            <p>👈 왼쪽에서 이미지를 먼저 업로드해주세요</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 캔버스 설정
    platform = SessionManager.get("selected_platform")
    canvas_ratio = SessionManager.get("canvas_ratio")
    canvas_size = config.CANVAS_RATIOS.get(canvas_ratio, config.DEFAULT_CANVAS_SIZE)
    
    st.info(f"📱 {platform} | {canvas_ratio} ({canvas_size[0]}×{canvas_size[1]})")
    
    # 조정 컨트롤
    render_positioning_controls(api_client, bg_removed, canvas_size)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_positioning_controls(api_client, bg_removed_image, canvas_size):
    """배치 조정 컨트롤"""
    st.markdown("#### ⚙️ 배치 설정")
    
    # 현재 값들
    current_scale = SessionManager.get("product_scale", 10)
    current_x = SessionManager.get("product_x", 200)
    current_y = SessionManager.get("product_y", 200)
    
    # 슬라이더
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scale = st.slider("크기", 1, 20, current_scale, key="scale_slider")
    with col2:
        x_pos = st.slider("X 위치", 0, 400, current_x, key="x_slider")
    with col3:
        y_pos = st.slider("Y 위치", 0, 400, current_y, key="y_slider")
    
    # 값이 변경되었을 때만 API 호출
    if (scale != current_scale or x_pos != current_x or y_pos != current_y):
        SessionManager.update({
            "product_scale": scale,
            "product_x": x_pos,
            "product_y": y_pos
        })
        
        with st.spinner("🔄 배치를 조정하고 있습니다..."):
            result = api_client.position_product(
                image=bg_removed_image,
                canvas_size=canvas_size,
                scale=scale * 10,  # API는 퍼센트 단위
                position=(x_pos - 200, y_pos - 200)
            )
            
            if result:
                SessionManager.update({
                    "positioned_image": result['positioned_image'],
                    "mask_image": result['mask_image']
                })
    
    # 결과 미리보기
    positioned = SessionManager.get("positioned_image")
    mask = SessionManager.get("mask_image")
    
    if positioned and mask:
        st.markdown("#### 🖼️ 배치 미리보기")
        
        tab1, tab2 = st.tabs(["배치 결과", "마스크"])
        
        with tab1:
            st.image(positioned, caption="배치된 제품", use_container_width=True)
        
        with tab2:
            st.image(mask, caption="생성된 마스크", use_container_width=True)
        
        # 저장 버튼
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 이미지 저장", type="secondary"):
                save_positioned_image(positioned)
        
        with col2:
            img_bytes = BytesIO()
            positioned.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            st.download_button(
                label="📥 다운로드",
                data=img_bytes,
                file_name="positioned_product.png",
                mime="image/png"
            )

def save_positioned_image(image):
    """배치된 이미지 저장"""
    try:
        save_path = config.get_image_path() / "temp" / "positioned_product.png"
        save_path.parent.mkdir(exist_ok=True)
        image.save(save_path)
        st.success(f"✅ 이미지가 저장되었습니다: {save_path.name}")
    except Exception as e:
        st.error(f"저장 중 오류 발생: {str(e)}")