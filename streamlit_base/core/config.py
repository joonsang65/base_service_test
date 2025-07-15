"""Streamlit 앱 설정 관리"""
import os
from typing import Dict, Any
from pathlib import Path

class StreamlitConfig:
    """Streamlit 앱 전체 설정"""
    
    # FastAPI 연결 설정
    FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")
    
    # 페이지 설정
    PAGE_TITLE = "AI 광고 제작 플랫폼"
    PAGE_ICON = "🎨"
    LAYOUT = "wide"
    
    # 파일 업로드 설정
    MAX_UPLOAD_SIZE = 10  # MB
    ALLOWED_IMAGE_TYPES = ["png", "jpg", "jpeg"]
    
    # 캔버스 설정
    DEFAULT_CANVAS_SIZE = (512, 512)
    CANVAS_RATIOS = {
        "🖼️ 가로형 (4:3)": (720, 512),
        "📱 세로형 (3:4)": (512, 720),
        "📐 정사각형 (1:1)": (512, 512),
    }
    
    # 플랫폼별 설정
    PLATFORMS = {
        "인스타그램": {
            "default_ratio": "📐 정사각형 (1:1)",
            "category": "social"
        },
        "블로그": {
            "default_ratio": "🖼️ 가로형 (4:3)",
            "category": "blog"
        },
        "포스터": {
            "default_ratio": "📱 세로형 (3:4)",
            "category": "print"
        }
    }
    
    # 스타일 설정
    PRIMARY_COLOR = "#4A8CF1"
    SECONDARY_COLOR = "#F4F6FA"
    SUCCESS_COLOR = "#28a745"
    WARNING_COLOR = "#ffc107"
    ERROR_COLOR = "#dc3545"
    
    @classmethod
    def get_static_path(cls) -> Path:
        """정적 파일 경로 반환"""
        return Path(__file__).parent.parent / "static"
    
    @classmethod
    def get_image_path(cls) -> Path:
        """이미지 경로 반환"""
        return cls.get_static_path() / "images"

config = StreamlitConfig()