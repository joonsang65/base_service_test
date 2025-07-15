"""텍스트 스타일링 폼"""
import streamlit as st
from core.session_manager import SessionManager
from utils.constants import AVAILABLE_FONTS

def render_text_styling_form(api_client):
    """텍스트 스타일링 폼 렌더링"""
    
    generated_text = SessionManager.get("generated_text")
    if not generated_text:
        st.info("먼저 광고 문구를 생성해주세요.")
        return
    
    with st.form("text_styling_form", clear_on_submit=False):
        st.markdown("#### 🎨 폰트 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            font_name = st.selectbox(
                "폰트 선택",
                options=list(AVAILABLE_FONTS.keys()),
                index=0,
                help="원하는 폰트를 선택하세요"
            )
            
            font_size = st.slider(
                "폰트 크기",
                min_value=20,
                max_value=200,
                value=SessionManager.get("font_size", 80),
                step=5,
                help="텍스트의 크기를 조정하세요"
            )
        
        with col2:
            stroke_width = st.slider(
                "테두리 굵기",
                min_value=0,
                max_value=10,
                value=SessionManager.get("stroke_width", 2),
                step=1,
                help="텍스트 테두리의 굵기를 설정하세요"
            )
            
            text_align = st.selectbox(
                "텍스트 정렬",
                ["center", "left", "right"],
                index=0,
                help="텍스트 정렬 방식을 선택하세요"
            )
        
        st.markdown("#### 🌈 색상 설정")
        
        # 색상 프리셋
        color_presets = {
            "클래식": {"text": "#000000", "stroke": "#FFFFFF"},
            "모던": {"text": "#2C3E50", "stroke": "#ECF0F1"},
            "활력": {"text": "#E74C3C", "stroke": "#FFFFFF"},
            "자연": {"text": "#27AE60", "stroke": "#FFFFFF"},
            "하늘": {"text": "#3498DB", "stroke": "#FFFFFF"},
            "선셋": {"text": "#F39C12", "stroke": "#2C3E50"},
            "럭셔리": {"text": "#8E44AD", "stroke": "#F1C40F"},
            "직접 설정": {"text": "#000000", "stroke": "#FFFFFF"}
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_preset = st.selectbox(
                "색상 프리셋",
                list(color_presets.keys()),
                help="미리 설정된 색상 조합을 선택하거나 직접 설정하세요"
            )
        
        # 선택된 프리셋에 따른 색상 설정
        if selected_preset == "직접 설정":
            with col2:
                text_color = st.color_picker(
                    "텍스트 색상",
                    value=SessionManager.get("text_color", "#000000"),
                    help="텍스트의 메인 색상을 선택하세요"
                )
            
            with col3:
                stroke_color = st.color_picker(
                    "테두리 색상",
                    value=SessionManager.get("stroke_color", "#FFFFFF"),
                    help="텍스트 테두리 색상을 선택하세요"
                )
        else:
            preset_colors = color_presets[selected_preset]
            text_color = preset_colors["text"]
            stroke_color = preset_colors["stroke"]
            
            with col2:
                st.markdown(f"**텍스트 색상:** <span style='color: {text_color}'>●</span> {text_color}", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**테두리 색상:** <span style='color: {stroke_color}'>●# 완전한 Streamlit 파일 구조")