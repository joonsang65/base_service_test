"""4단계: 최종 합성"""
import streamlit as st
from PIL import Image
from io import BytesIO
from datetime import datetime
from core.session_manager import SessionManager
from core.config import config
from utils.styles import WORKFLOW_CSS
from components.ui.navigation import render_step_navigation, render_breadcrumb
from widgets.image_editor import render_text_position_editor

def render():
    """4단계 메인 렌더링 함수"""
    st.markdown(WORKFLOW_CSS, unsafe_allow_html=True)
    
    platform = SessionManager.get("selected_platform")
    
    # 브레드크럼
    render_breadcrumb(4, platform)
    
    # 헤더
    st.markdown("""
    <div class="step-header">
        <h2>4️⃣ 최종 광고 완성</h2>
        <p>텍스트 위치를 조정하고 최종 광고를 완성합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 필요한 이미지들 확인
    background_img = SessionManager.get("selected_background")
    text_img = SessionManager.get("text_image")
    
    if not background_img:
        st.error("❌ 배경 이미지가 없습니다.")
        render_error_navigation(2, "2단계에서 배경을 먼저 생성해주세요.")
        return
    
    if not text_img:
        st.error("❌ 텍스트 이미지가 없습니다.")
        render_error_navigation(3, "3단계에서 텍스트를 먼저 생성해주세요.")
        return
    
    # 메인 컨텐츠
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_final_preview_section(background_img, text_img)
    
    with col2:
        render_text_adjustment_section()
    
    # 완성 섹션
    render_completion_section(background_img, text_img)
    
    # 네비게이션
    render_step_navigation(
        current_step=4,
        can_proceed=True
    )

def render_error_navigation(target_step, message):
    """에러 상황에서의 네비게이션"""
    st.warning(message)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(f"⬅️ {target_step}단계로 이동", type="primary"):
            SessionManager.set("current_step", target_step)
            st.rerun()

def render_final_preview_section(background_img, text_img):
    """최종 미리보기 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("🖼️ 실시간 미리보기")
    
    # 현재 설정값들
    text_scale = SessionManager.get("text_scale", 50) / 100
    text_x = SessionManager.get("text_x", 0)
    text_y = SessionManager.get("text_y", -100)
    
    # 이미지 합성
    composed_image = compose_final_image(background_img, text_img, text_scale, text_x, text_y)
    
    # 미리보기 표시
    st.image(composed_image, caption="최종 광고 미리보기", use_container_width=True)
    
    # 이미지 정보
    st.info(f"📐 크기: {composed_image.size[0]} × {composed_image.size[1]} 픽셀")
    
    # 세션에 최종 이미지 저장
    SessionManager.set("final_image", composed_image)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_text_adjustment_section():
    """텍스트 조정 섹션"""
    st.markdown('<div class="process-box">', unsafe_allow_html=True)
    st.subheader("🎛️ 텍스트 위치 조정")
    
    # 텍스트 위치 에디터 위젯 사용
    render_text_position_editor()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_completion_section(background_img, text_img):
    """완성 섹션"""
    st.markdown("---")
    st.markdown('<div class="process-box status-success">', unsafe_allow_html=True)
    st.subheader("🎉 광고 완성")
    
    final_image = SessionManager.get("final_image")
    
    if final_image:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 최종 저장", type="primary", use_container_width=True):
                save_final_advertisement(final_image)
        
        with col2:
            # 다운로드 버튼
            img_bytes = BytesIO()
            final_image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"advertisement_{timestamp}.png"
            
            st.download_button(
                label="📥 다운로드",
                data=img_bytes,
                file_name=filename,
                mime="image/png",
                type="primary",
                use_container_width=True
            )
        
        with col3:
            if st.button("📤 갤러리에 추가", type="secondary", use_container_width=True):
                add_to_gallery(final_image)
    
    st.markdown('</div>', unsafe_allow_html=True)

def compose_final_image(background_img, text_img, scale, x_offset, y_offset):
    """최종 이미지 합성"""
    # 배경 이미지 복사
    final_img = background_img.copy()
    
    # 텍스트 이미지 크기 조정
    text_width = int(text_img.width * scale)
    text_height = int(text_img.height * scale)
    resized_text = text_img.resize((text_width, text_height), Image.Resampling.LANCZOS)
    
    # 붙여넣기 위치 계산 (중앙 기준)
    paste_x = (final_img.width - text_width) // 2 + x_offset
    paste_y = (final_img.height - text_height) // 2 + y_offset
    
    # 이미지 경계 확인 및 조정
    paste_x = max(0, min(paste_x, final_img.width - text_width))
    paste_y = max(0, min(paste_y, final_img.height - text_height))
    
    # 알파 채널 고려하여 합성
    if resized_text.mode == 'RGBA':
        final_img.paste(resized_text, (paste_x, paste_y), resized_text)
    else:
        final_img.paste(resized_text, (paste_x, paste_y))
    
    return final_img

def save_final_advertisement(image):
    """최종 광고 저장"""
    try:
        # 저장 경로 설정
        save_dir = config.get_image_path() / "completed"
        save_dir.mkdir(exist_ok=True)
        
        # 파일명 생성
        platform = SessionManager.get("selected_platform", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{timestamp}.png"
        
        # 저장
        save_path = save_dir / filename
        image.save(save_path, format="PNG", quality=95)
        
        st.success(f"✅ 최종 광고가 저장되었습니다: {filename}")
        
        # 통계 업데이트 (선택사항)
        update_completion_stats(platform)
        
    except Exception as e:
        st.error(f"저장 중 오류 발생: {str(e)}")

def add_to_gallery(image):
    """갤러리에 이미지 추가"""
    try:
        platform = SessionManager.get("selected_platform", "unknown").lower()
        gallery_dir = config.get_image_path() / "gallery" / platform
        gallery_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ad_{timestamp}.png"
        
        save_path = gallery_dir / filename
        image.save(save_path, format="PNG")
        
        st.success("✅ 갤러리에 추가되었습니다!")
        
    except Exception as e:
        st.error(f"갤러리 추가 중 오류 발생: {str(e)}")

def update_completion_stats(platform):
    """완성 통계 업데이트"""
    # 간단한 통계 파일 업데이트 (선택사항)
    try:
        stats_file = config.get_static_path() / "stats.json"
        import json
        
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {"total_completed": 0, "by_platform": {}}
        
        stats["total_completed"] = stats.get("total_completed", 0) + 1
        stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f)
            
    except Exception:
        pass  # 통계 실패해도 메인 기능에 영향 없음