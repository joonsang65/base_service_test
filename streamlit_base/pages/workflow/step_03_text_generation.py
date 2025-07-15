"""3단계: 텍스트 생성"""
import streamlit as st
from PIL import Image
from io import BytesIO
from core.session_manager import SessionManager
from core.config import config
from services.api_client import get_api_client
from utils.styles import WORKFLOW_CSS
from components.ui.navigation import render_step_navigation, render_breadcrumb
from forms.product_forms import render_product_info_form
from forms.text_form import render_text_styling_form

def render():
    """3단계 메인 렌더링 함수"""
    st.markdown(WORKFLOW_CSS, unsafe_allow_html=True)
    
    api_client = get_api_client()
    platform = SessionManager.get("selected_platform")
    
    # 브레드크럼
    render_breadcrumb(3, platform)
    
    # 헤더
    st.markdown("""
    <div class="step-header">
        <h2>3️⃣ 광고 텍스트 생성</h2>
        <p>제품 정보를 입력하고 AI가 매력적인 광고 문구를 생성합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 메인 컨텐츠
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_product_input_section(api_client)
    
    with col2:
        render_text_preview_section(api_client)
    
    # 네비게이션
    render_step_navigation(
        current_step=3,
        can_proceed=SessionManager.can_proceed_to_step(4),
        proceed_message="텍스트 이미지를 먼저 생성해주세요."
    )

def render_product_input_section(api_client):
    """제품 정보 입력 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("📝 제품 정보 입력")
    
    # 제품 정보 폼
    render_product_info_form(api_client)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_text_preview_section(api_client):
    """텍스트 미리보기 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("📱 텍스트 미리보기")
    
    generated_text = SessionManager.get("generated_text")
    
    if not generated_text:
        st.markdown("""
        <div class="image-preview">
            <p>👈 왼쪽에서 제품 정보를 입력하고 텍스트를 생성해주세요</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 생성된 텍스트 표시
    st.markdown("#### ✨ 생성된 광고 문구")
    st.success(generated_text)
    
    # 텍스트 재생성 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 생성", type="secondary"):
            regenerate_text(api_client)
    
    with col2:
        if st.button("✏️ 직접 수정"):
            SessionManager.set("text_edit_mode", True)
            st.rerun()
    
    # 텍스트 직접 수정 모드
    if SessionManager.get("text_edit_mode", False):
        render_text_edit_mode()
    
    st.markdown("---")
    
    # 텍스트 스타일링
    render_text_styling_section(api_client)
    
    st.markdown('</div>', unsafe_allow_html=True)

def regenerate_text(api_client):
    """텍스트 재생성"""
    product_name = SessionManager.get("product_name")
    product_usage = SessionManager.get("product_usage")
    brand_name = SessionManager.get("brand_name")
    additional_info = SessionManager.get("additional_info")
    
    if not all([product_name, product_usage, brand_name]):
        st.error("제품 정보를 다시 확인해주세요.")
        return
    
    with st.spinner("🤖 새로운 광고 문구를 생성하고 있습니다..."):
        try:
            generated_text = api_client.generate_ad_text(
                product_name=product_name,
                product_usage=product_usage,
                brand_name=brand_name,
                additional_info=additional_info
            )
            
            if generated_text:
                SessionManager.set("generated_text", generated_text)
                st.success("✅ 새로운 광고 문구가 생성되었습니다!")
                st.rerun()
            else:
                st.error("텍스트 생성에 실패했습니다.")
                
        except Exception as e:
            st.error(f"텍스트 생성 중 오류 발생: {str(e)}")

def render_text_edit_mode():
    """텍스트 직접 수정 모드"""
    st.markdown("#### ✏️ 텍스트 직접 수정")
    
    current_text = SessionManager.get("generated_text", "")
    edited_text = st.text_area(
        "광고 문구를 수정하세요",
        value=current_text,
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 수정 완료"):
            SessionManager.set("generated_text", edited_text)
            SessionManager.set("text_edit_mode", False)
            st.success("텍스트가 수정되었습니다!")
            st.rerun()
    
    with col2:
        if st.button("❌ 취소"):
            SessionManager.set("text_edit_mode", False)
            st.rerun()

def render_text_styling_section(api_client):
    """텍스트 스타일링 섹션"""
    st.markdown("#### 🎨 텍스트 스타일링")
    
    # 텍스트 스타일링 폼
    render_text_styling_form(api_client)
    
    # 텍스트 이미지 미리보기
    text_image = SessionManager.get("text_image")
    if text_image:
        st.markdown("#### 🖼️ 텍스트 이미지 미리보기")
        st.image(text_image, caption="생성된 텍스트 이미지", use_container_width=True)
        
        # 저장 및 다운로드
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 텍스트 이미지 저장", type="secondary"):
                save_text_image(text_image)
        
        with col2:
            img_bytes = BytesIO()
            text_image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            st.download_button(
                label="📥 다운로드",
                data=img_bytes,
                file_name="text_image.png",
                mime="image/png"
            )

def save_text_image(image):
    """텍스트 이미지 저장"""
    try:
        save_path = config.get_image_path() / "temp" / "text_image.png"
        save_path.parent.mkdir(exist_ok=True)
        image.save(save_path)
        st.success(f"✅ 텍스트 이미지가 저장되었습니다!")
    except Exception as e:
        st.error(f"저장 중 오류 발생: {str(e)}")