"""네비게이션 컴포넌트"""
import streamlit as st
from core.session_manager import SessionManager

def render_step_navigation(current_step: int, can_proceed: bool = True, proceed_message: str = ""):
    """워크플로우 단계 네비게이션"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_step > 1:
            if st.button("⬅️ 이전 단계", type="secondary"):
                SessionManager.set("current_step", current_step - 1)
                st.rerun()
        else:
            st.button("⬅️ 이전 단계", disabled=True)
    
    with col2:
        if not can_proceed and proceed_message:
            st.warning(proceed_message)
        elif can_proceed:
            st.success("✅ 다음 단계로 진행할 수 있습니다")
    
    with col3:
        if current_step < 4:
            if st.button("➡️ 다음 단계", type="primary", disabled=not can_proceed):
                if can_proceed:
                    SessionManager.set("current_step", current_step + 1)
                    st.rerun()
        else:
            if st.button("🏠 완료", type="primary"):
                SessionManager.reset_all()
                SessionManager.set("current_page", "home")
                st.rerun()

def render_breadcrumb(current_step: int, platform: str):
    """단계별 브레드크럼"""
    steps = [
        {"num": 1, "name": "제품 설정", "icon": "📤"},
        {"num": 2, "name": "배경 생성", "icon": "🎨"}, 
        {"num": 3, "name": "텍스트 생성", "icon": "✍️"},
        {"num": 4, "name": "최종 완성", "icon": "🎯"}
    ]
    
    breadcrumb_html = f"""
    <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
        <div style="font-size: 14px; color: #666; margin-bottom: 8px;">
            📱 {platform} 광고 제작
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
    """
    
    for i, step in enumerate(steps):
        if step["num"] < current_step:
            status_class = "completed"
            color = "#28a745"
        elif step["num"] == current_step:
            status_class = "current"
            color = "#4A8CF1"
        else:
            status_class = "pending"
            color = "#6c757d"
        
        breadcrumb_html += f"""
            <div style="display: flex; align-items: center; color: {color};">
                <span style="font-size: 16px;">{step['icon']}</span>
                <span style="margin-left: 4px; font-weight: {'bold' if step['num'] == current_step else 'normal'};">
                    {step['name']}
                </span>
            </div>
        """
        
        if i < len(steps) - 1:
            breadcrumb_html += '<span style="margin: 0 8px; color: #dee2e6;">›</span>'
    
    breadcrumb_html += """
        </div>
    </div>
    """
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)