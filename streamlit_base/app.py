"""Streamlit 메인 앱"""
import streamlit as st
from core.config import config
from core.session_manager import SessionManager
from components.ui.slidebar import render_sidebar

# 페이지 기본 설정
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# 세션 초기화
SessionManager.initialize()

# 사이드바 렌더링
render_sidebar()

# 메인 페이지 라우팅
current_page = SessionManager.get("current_page", "home")

if current_page == "home":
    from pages.home import render
    render()

elif current_page == "gallery":
    from pages.gallery import render
    render()

elif current_page == "workflow":
    platform = SessionManager.get("selected_platform")
    
    if not platform:
        st.warning("⚠️ 사이드바에서 플랫폼을 먼저 선택해주세요.")
        st.stop()
    
    # 워크플로우 단계별 렌더링
    from components.ui.navigation import render_breadcrumb
    
    current_step = SessionManager.get("current_step", 1)
    render_breadcrumb(current_step, platform)
    
    if current_step == 1:
        from pages.workflow.step_01_product_setup import render
        render()
    elif current_step == 2:
        from pages.workflow.step_02_background_gengeration import render
        render()
    elif current_step == 3:
        from pages.workflow.step_03_text_generation import render
        render()
    elif current_step == 4:
        from pages.workflow.step_04_final_composition import render
        render()

# 하단 푸터
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 12px; padding: 20px;">
        🎨 AI 광고 제작 플랫폼 | Made with codeit_AI_team2
    </div>
    """,
    unsafe_allow_html=True
)