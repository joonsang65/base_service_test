"""이미지 편집 위젯"""
import streamlit as st
from core.session_manager import SessionManager

def render_text_position_editor():
    """텍스트 위치 조정 에디터"""
    
    st.markdown("#### 📐 위치 및 크기 조정")
    
    # 현재 값들 가져오기
    current_scale = SessionManager.get("text_scale", 50)
    current_x = SessionManager.get("text_x", 0)
    current_y = SessionManager.get("text_y", -100)
    
    # 슬라이더들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        scale = st.slider(
            "크기 (%)",
            min_value=10,
            max_value=200,
            value=current_scale,
            step=5,
            help="텍스트의 크기를 조정합니다"
        )
    
    with col2:
        x_pos = st.slider(
            "가로 위치",
            min_value=-300,
            max_value=300,
            value=current_x,
            step=10,
            help="텍스트의 가로 위치를 조정합니다"
        )
    
    with col3:
        y_pos = st.slider(
            "세로 위치",
            min_value=-300,
            max_value=300,
            value=current_y,
            step=10,
            help="텍스트의 세로 위치를 조정합니다"
        )
    
    # 값이 변경되었는지 확인
    if (scale != current_scale or x_pos != current_x or y_pos != current_y):
        SessionManager.update({
            "text_scale": scale,
            "text_x": x_pos,
            "text_y": y_pos
        })
        st.rerun()
    
    # 빠른 위치 설정 버튼들
    st.markdown("#### ⚡ 빠른 설정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬆️ 상단", use_container_width=True):
            SessionManager.update({"text_x": 0, "text_y": -150})
            st.rerun()
    
    with col2:
        if st.button("🎯 중앙", use_container_width=True):
            SessionManager.update({"text_x": 0, "text_y": 0})
            st.rerun()
    
    with col3:
        if st.button("⬇️ 하단", use_container_width=True):
            SessionManager.update({"text_x": 0, "text_y": 150})
            st.rerun()
    
    # 미세 조정 버튼들
    st.markdown("#### 🎛️ 미세 조정")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⬅️", help="왼쪽으로 5px"):
            SessionManager.set("text_x", SessionManager.get("text_x", 0) - 5)
            st.rerun()
    
    with col2:
        if st.button("⬆️", help="위로 5px"):
            SessionManager.set("text_y", SessionManager.get("text_y", 0) - 5)
            st.rerun()
    
    with col3:
        if st.button("🔄", help="초기화"):
            SessionManager.update({"text_scale": 50, "text_x": 0, "text_y": -100})
            st.rerun()
    
    with col4:
        if st.button("⬇️", help="아래로 5px"):
            SessionManager.set("text_y", SessionManager.get("text_y", 0) + 5)
            st.rerun()
    
    with col5:
        if st.button("➡️", help="오른쪽으로 5px"):
            SessionManager.set("text_x", SessionManager.get("text_x", 0) + 5)
            st.rerun()
    
    # 현재 설정값 표시
    st.markdown("---")
    st.markdown(f"**현재 설정:** 크기 {scale}%, 위치 ({x_pos}, {y_pos})")

def render_image_preview_widget(image, caption="미리보기"):
    """이미지 미리보기 위젯"""
    if image:
        st.image(image, caption=caption, use_container_width=True)
        
        # 이미지 정보
        st.caption(f"크기: {image.size[0]} × {image.size[1]} 픽셀")
    else:
        st.info("이미지가 없습니다.")

def render_canvas_widget(width=512, height=512):
    """캔버스 위젯"""
    from streamlit_drawable_canvas import st_canvas
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="freedraw",
        key="canvas_widget"
    )
    
    return canvas_result