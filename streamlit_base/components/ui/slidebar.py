"""사이드바 네비게이션 컴포넌트"""
import streamlit as st
from streamlit_option_menu import option_menu
from core.session_manager import SessionManager
from core.config import config
from utils.styles import SIDEBAR_STYLES

def render_sidebar():
    """사이드바 메뉴 렌더링"""
    
    # 현재 페이지에 따른 기본 인덱스 설정
    page_to_index = {
        "home": 0,
        "gallery": 1,
        "workflow": 2
    }
    
    current_page = SessionManager.get("current_page", "home")
    default_index = page_to_index.get(current_page, 0)
    
    with st.sidebar:
        selected = option_menu(
            menu_title="AI 광고 제작",
            options=["홈", "갤러리", "광고 생성"],
            icons=["house-fill", "images", "magic"],
            menu_icon="palette-fill",
            default_index=default_index,
            styles=SIDEBAR_STYLES,
        )
        
        # 페이지 매핑
        page_mapping = {
            "홈": "home",
            "갤러리": "gallery", 
            "광고 생성": "workflow"
        }
        
        selected_page = page_mapping[selected]
        
        # 광고 생성 페이지일 때 플랫폼 선택
        if selected == "광고 생성":
            st.markdown("---")
            render_platform_selector()
            
            # 진행 상황 표시
            if SessionManager.get("selected_platform"):
                render_progress_indicator()
        
        # 페이지 변경 처리
        if current_page != selected_page:
            SessionManager.set("current_page", selected_page)
            if selected_page != "workflow":
                SessionManager.set("selected_platform", None)
                SessionManager.set("current_step", 1)
            st.rerun()

def render_platform_selector():
    """플랫폼 선택 UI"""
    st.markdown("### 📱 플랫폼 선택")
    
    platform_options = ["플랫폼을 선택하세요"] + list(config.PLATFORMS.keys())
    current_platform = SessionManager.get("selected_platform")
    
    # 현재 선택된 플랫폼의 인덱스 찾기
    try:
        default_index = platform_options.index(current_platform) if current_platform else 0
    except ValueError:
        default_index = 0
    
    selected_platform = st.selectbox(
        "플랫폼",
        platform_options,
        index=default_index,
        label_visibility="collapsed"
    )
    
    if selected_platform != "플랫폼을 선택하세요" and selected_platform != current_platform:
        SessionManager.update({
            "selected_platform": selected_platform,
            "current_step": 1
        })
        
        # 플랫폼별 기본 설정 적용
        platform_config = config.PLATFORMS[selected_platform]
        SessionManager.set("canvas_ratio", platform_config["default_ratio"])
        st.rerun()

def render_progress_indicator():
    """진행 상황 표시"""
    st.markdown("### 📊 진행 상황")
    
    current_step = SessionManager.get("current_step", 1)
    
    steps = [
        "1️⃣ 제품 이미지",
        "2️⃣ 배경 생성", 
        "3️⃣ 텍스트 생성",
        "4️⃣ 최종 완성"
    ]
    
    for i, step_name in enumerate(steps, 1):
        if i < current_step:
            st.success(f"✅ {step_name}")
        elif i == current_step:
            st.info(f"▶️ {step_name}")
        else:
            st.write(f"⏳ {step_name}")