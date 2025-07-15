"""세션 상태 관리"""
import streamlit as st
from typing import Any, Dict, Optional

class SessionManager:
    """Streamlit 세션 상태 통합 관리"""
    
    # 기본 세션 키들
    DEFAULT_KEYS = {
        # 네비게이션
        "current_page": "home",
        "current_step": 1,
        "selected_platform": None,
        
        # 1단계: 제품 이미지
        "upload_mode": "직접 업로드",
        "original_image": None,
        "bg_removed_image": None,
        "positioned_image": None,
        "mask_image": None,
        "product_scale": 10,
        "product_x": 200,
        "product_y": 200,
        
        # 2단계: 배경 생성
        "generation_mode": "🎨 자연스럽게 합성하기(generate)",
        "canvas_ratio": "📐 정사각형 (1:1)",
        "bg_prompt": "",
        "reference_image": None,
        "generated_backgrounds": None,
        "selected_background": None,
        
        # 3단계: 텍스트 생성
        "product_name": "",
        "product_usage": "",
        "brand_name": "",
        "additional_info": "",
        "generated_text": "",
        "text_image": None,
        "font_settings": {},
        
        # 4단계: 최종 합성
        "text_scale": 50,
        "text_x": 0,
        "text_y": -100,
        "final_image": None,
        
        # 상태 플래그
        "is_processing": False,
        "last_error": None,
    }
    
    @classmethod
    def initialize(cls):
        """세션 상태 초기화"""
        for key, default_value in cls.DEFAULT_KEYS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """세션 값 가져오기"""
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any):
        """세션 값 설정"""
        st.session_state[key] = value
    
    @classmethod
    def update(cls, updates: Dict[str, Any]):
        """여러 세션 값 한번에 업데이트"""
        for key, value in updates.items():
            st.session_state[key] = value
    
    @classmethod
    def reset_step(cls, step: int):
        """특정 단계 관련 세션 초기화"""
        step_keys = {
            1: ["original_image", "bg_removed_image", "positioned_image", "mask_image"],
            2: ["generated_backgrounds", "selected_background", "bg_prompt"],
            3: ["generated_text", "text_image", "product_name", "product_usage", "brand_name"],
            4: ["final_image"]
        }
        
        for key in step_keys.get(step, []):
            if key in cls.DEFAULT_KEYS:
                st.session_state[key] = cls.DEFAULT_KEYS[key]
    
    @classmethod
    def reset_all(cls):
        """모든 세션 초기화"""
        for key in cls.DEFAULT_KEYS:
            st.session_state[key] = cls.DEFAULT_KEYS[key]
    
    @classmethod
    def can_proceed_to_step(cls, step: int) -> bool:
        """다음 단계로 진행 가능한지 확인"""
        requirements = {
            2: cls.get("positioned_image") is not None,
            3: cls.get("selected_background") is not None,
            4: cls.get("text_image") is not None,
        }
        return requirements.get(step, True)