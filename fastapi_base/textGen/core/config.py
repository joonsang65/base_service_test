from pydantic_settings import BaseSettings
from textGen.utils.prompts import *

from typing import List, Dict, Any, Optional

import os

class Settings(BaseSettings):
    # 앱 기본 설정
    APP_NAME: str = "광고 문구 생성 API"
    APP_DESCRIPTION: str = "OpenAI를 활용한 다양한 플랫폼의 광고 문구 생성 서비스"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # OpenAI 설정
    OPENAI_API_KEY: Optional[str] = None
    
    # 모델 설정
    DEFAULT_MODEL_MINI: str = "gpt-4.1-mini"
    DEFAULT_TEMPERATURES: List[float] = [0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    
    # 지원 플랫폼
    SUPPORTED_PLATFORMS: List[str] = ["인스타그램", "블로그", "포스터"]
    
    # 모드 설정
    PLATFORM_MODES: Dict[str, List[Optional[str]]] = {
        "인스타그램": ["1", "2"],
        "블로그": ["1", "2"],
        "포스터": [None]
    }
    
    MODE_DESCRIPTIONS: Dict[str, str] = {
        "1": "광고 문구만 생성",
        "2": "광고 문구 + 텍스트 이미지용 문구 생성"
    }
    
    # 환경 변수 파일 경로
    DEFAULT_ENV_PATH: str = "..env"
    
    class Config:
        env_file = "..env"
        case_sensitive = True
        extra = "ignore"  # ✅ 추가: 정의되지 않은 필드 무시

# 설정 인스턴스 생성
settings = Settings()

# 기존 models.py와의 호환성을 위한 변수들
DEFAULT_MODEL = {
    "mini": settings.DEFAULT_MODEL_MINI
}

DEFAULT_TEMPERATURES = settings.DEFAULT_TEMPERATURES
DEFAULT_ENV_PATH = settings.DEFAULT_ENV_PATH

PROMPT_CONFIGS = {
    "인스타그램": (system_prompt_insta, few_shot_examples_insta),
    "블로그": (system_prompt_blog, few_shot_examples_blog),
    "포스터": (system_prompt_TI, few_shot_examples_TI)
}