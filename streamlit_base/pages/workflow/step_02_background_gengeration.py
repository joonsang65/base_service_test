"""2단계: 배경 생성"""
import streamlit as st
from PIL import Image
from core.session_manager import SessionManager
from core.config import config
from services.api_client import get_api_client
from utils.styles import WORKFLOW_CSS
from components.ui.navigation import render_step_navigation, render_breadcrumb

def render():
    """2단계 메인 렌더링 함수"""
    st.markdown(WORKFLOW_CSS, unsafe_allow_html=True)
    
    api_client = get_api_client()
    platform = SessionManager.get("selected_platform")
    
    # 브레드크럼
    render_breadcrumb(2, platform)
    
    # 헤더
    st.markdown("""
    <div class="step-header">
        <h2>2️⃣ 배경 이미지 생성</h2>
        <p>AI가 제품에 어울리는 배경을 생성합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 설정 섹션
    render_generation_settings()
    
    st.markdown("---")
    
    # 생성 섹션
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_prompt_input_section(api_client)
    
    with col2:
        render_background_preview_section(api_client)
    
    # 네비게이션
    render_step_navigation(
        current_step=2,
        can_proceed=SessionManager.can_proceed_to_step(3),
        proceed_message="배경 이미지를 먼저 생성하고 선택해주세요."
    )

def render_generation_settings():
    """생성 설정 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("⚙️ 생성 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 생성 방식")
        generation_mode = st.radio(
            "선택하세요",
            ["🖌️ 제품 그대로 붙이기 (Inpaint)", "🎨 자연스럽게 합성하기 (Generate)"],
            horizontal=False,
            help="Inpaint: 제품 위치 그대로 배경만 생성\nGenerate: 제품과 배경을 자연스럽게 합성"
        )
        SessionManager.set("generation_mode", generation_mode)
    
    with col2:
        st.markdown("#### 📐 이미지 비율")
        canvas_ratio = st.selectbox(
            "출력 비율을 선택하세요",
            list(config.CANVAS_RATIOS.keys()),
            index=list(config.CANVAS_RATIOS.keys()).index(
                SessionManager.get("canvas_ratio", "📐 정사각형 (1:1)")
            )
        )
        SessionManager.set("canvas_ratio", canvas_ratio)
        
        # 선택된 비율 정보 표시
        width, height = config.CANVAS_RATIOS[canvas_ratio]
        st.info(f"📏 {width} × {height} 픽셀")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_prompt_input_section(api_client):
    """프롬프트 입력 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("✍️ 배경 설명 입력")
    
    # GPT 자동 분석 섹션
    render_gpt_analysis_section(api_client)
    
    st.markdown("---")
    
    # 수동 프롬프트 입력
    st.markdown("#### 📝 배경 프롬프트 (직접 입력)")
    
    bg_prompt = st.text_area(
        "원하는 배경을 설명해주세요",
        value=SessionManager.get("bg_prompt", ""),
        placeholder="예: 따뜻한 햇살이 비치는 카페 테라스, 나무 테이블 위",
        height=100,
        help="구체적으로 설명할수록 더 정확한 결과를 얻을 수 있습니다."
    )
    SessionManager.set("bg_prompt", bg_prompt)
    
    # 참조 이미지 업로드
    st.markdown("#### 🖼️ 참조 이미지 (선택사항)")
    reference_image = st.file_uploader(
        "스타일 참조용 이미지를 업로드하세요",
        type=config.ALLOWED_IMAGE_TYPES,
        help="업로드한 이미지의 스타일을 참고하여 배경을 생성합니다."
    )
    
    if reference_image:
        ref_img = Image.open(reference_image)
        SessionManager.set("reference_image", ref_img)
        st.image(ref_img, caption="참조 이미지", width=200)
    
    # 생성 버튼
    if st.button("🎨 배경 생성하기", type="primary", use_container_width=True):
        if bg_prompt.strip():
            generate_background(api_client, bg_prompt)
        else:
            st.warning("배경 설명을 입력해주세요.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_gpt_analysis_section(api_client):
    """GPT 자동 분석 섹션"""
    st.markdown("#### 🤖 AI 자동 분석")
    
    positioned_image = SessionManager.get("positioned_image")
    reference_image = SessionManager.get("reference_image")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if positioned_image:
            st.info("✅ 제품 이미지가 준비되었습니다. AI가 자동으로 분석할 수 있습니다.")
        else:
            st.warning("⚠️ 1단계에서 제품 이미지를 먼저 준비해주세요.")
    
    with col2:
        if st.button("🔍 AI 분석 시작", disabled=not positioned_image):
            if positioned_image:
                analyze_with_gpt(api_client, positioned_image, reference_image)

def analyze_with_gpt(api_client, positioned_image, reference_image):
    """GPT를 통한 제품 분석"""
    with st.spinner("🤖 AI가 제품을 분석하고 있습니다..."):
        try:
            platform = SessionManager.get("selected_platform", "인스타그램")
            
            analysis_result = api_client.analyze_advertisement(
                product_image=positioned_image,
                product_type="general",
                marketing_type=f"{platform} 광고용 배경 생성",
                reference_image=reference_image
            )
            
            if analysis_result:
                st.success("✅ AI 분석이 완료되었습니다!")
                
                # 분석 결과 표시
                with st.expander("📋 AI 분석 결과", expanded=True):
                    st.markdown("**광고 기획안:**")
                    st.write(analysis_result['ad_plan'])
                    
                    st.markdown("**생성된 프롬프트:**")
                    st.code(analysis_result['generated_prompt'])
                
                # 프롬프트 자동 입력
                SessionManager.set("bg_prompt", analysis_result['generated_prompt'])
                st.rerun()
            
        except Exception as e:
            st.error(f"AI 분석 중 오류가 발생했습니다: {str(e)}")

def generate_background(api_client, prompt):
    """배경 생성 실행"""
    generation_mode = SessionManager.get("generation_mode")
    canvas_ratio = SessionManager.get("canvas_ratio")
    canvas_size = config.CANVAS_RATIOS[canvas_ratio]
    
    with st.spinner("🎨 AI가 배경을 생성하고 있습니다... (약 30초 소요)"):
        try:
            if "Inpaint" in generation_mode:
                # Inpaint 모드
                positioned_image = SessionManager.get("positioned_image")
                mask_image = SessionManager.get("mask_image")
                
                if not positioned_image or not mask_image:
                    st.error("제품 이미지와 마스크가 필요합니다. 1단계를 먼저 완료해주세요.")
                    return
                
                generated_images = api_client.inpaint_background(
                    canvas_image=positioned_image,
                    mask_image=mask_image,
                    prompt=prompt,
                    category="general"
                )
            else:
                # Generate 모드
                generated_images = api_client.generate_background(
                    prompt=prompt,
                    canvas_size=canvas_size,
                    category="general"
                )
                
                # Generate 모드에서는 스무딩 적용
                if generated_images:
                    bg_removed_image = SessionManager.get("bg_removed_image")
                    if bg_removed_image:
                        smoothed_images = []
                        for bg_img in generated_images:
                            smoothed = api_client.apply_smoothing(
                                background_image=bg_img,
                                product_image=bg_removed_image,
                                prompt=prompt,
                                category="general"
                            )
                            if smoothed:
                                smoothed_images.append(smoothed)
                        
                        if smoothed_images:
                            generated_images = smoothed_images
            
            if generated_images:
                SessionManager.set("generated_backgrounds", generated_images)
                st.success(f"✅ {len(generated_images)}개의 배경이 생성되었습니다!")
                st.rerun()
            else:
                st.error("배경 생성에 실패했습니다. 다시 시도해주세요.")
                
        except Exception as e:
            st.error(f"배경 생성 중 오류가 발생했습니다: {str(e)}")

def render_background_preview_section(api_client):
    """배경 미리보기 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("🖼️ 생성 결과")
    
    generated_backgrounds = SessionManager.get("generated_backgrounds")
    
    if not generated_backgrounds:
        st.markdown("""
        <div class="image-preview">
            <p>👈 왼쪽에서 배경을 생성하면 여기에 표시됩니다</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # 생성된 이미지들 표시
    st.markdown(f"#### 📸 생성된 배경 ({len(generated_backgrounds)}개)")
    
    if len(generated_backgrounds) > 1:
        # 탭으로 여러 이미지 표시
        tabs = st.tabs([f"배경 {i+1}" for i in range(len(generated_backgrounds))])
        
        for i, (tab, img) in enumerate(zip(tabs, generated_backgrounds)):
            with tab:
                render_single_background_preview(img, i, api_client)
    else:
        # 단일 이미지
        render_single_background_preview(generated_backgrounds[0], 0, api_client)
    
    # 재생성 버튼
    st.markdown("---")
    if st.button("🔄 다시 생성하기", type="secondary"):
        SessionManager.set("generated_backgrounds", None)
        SessionManager.set("selected_background", None)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_single_background_preview(image, index, api_client):
    """단일 배경 미리보기"""
    st.image(image, caption=f"생성된 배경 {index+1}", use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"✅ 이 배경 선택", key=f"select_bg_{index}", type="primary"):
            SessionManager.set("selected_background", image)
            st.success(f"배경 {index+1}이 선택되었습니다!")
            st.rerun()
    
    with col2:
        # 다운로드 버튼
        from io import BytesIO
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        st.download_button(
            label="📥 다운로드",
            data=img_bytes,
            file_name=f"background_{index+1}.png",
            mime="image/png",
            key=f"download_bg_{index}"
        )