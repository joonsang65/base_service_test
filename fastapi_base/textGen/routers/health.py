from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
from textGen.schemas.textGen_schemas import HealthResponse, PlatformInfo
from textGen.core.config import settings
from textGen.models.models import OpenAIClient

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    시스템 헬스 체크
    """
    try:
        # OpenAI 클라이언트 초기화 테스트
        client = OpenAIClient()
        
        available_services = ["광고 문구 생성"]
        if settings.IMAGE_GENERATION_ENABLE:
            available_services.append("이미지 생성")
        
        return HealthResponse(
            status="healthy",
            message="모든 서비스가 정상적으로 작동 중입니다.",
            timestamp=datetime.now().isoformat(),
            available_services=available_services
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503, 
            detail="서비스를 사용할 수 없습니다. 환경 변수 및 API 키를 확인해주세요."
        )

@router.get("/platforms", response_model=PlatformInfo)
async def get_supported_platforms():
    """
    지원되는 플랫폼 및 설정 정보 조회
    """
    return PlatformInfo(
        platforms=settings.SUPPORTED_PLATFORMS,
        modes=settings.PLATFORM_MODES,
        mode_descriptions=settings.MODE_DESCRIPTIONS,
        default_temperatures=settings.DEFAULT_TEMPERATURES,
        image_generation_enabled=settings.IMAGE_GENERATION_ENABLED
    )

@router.get("/status")
async def get_system_status():
    """
    시스템 상태 상세 정보
    """
    try:
        return {
            "app_name": settings.APP_NAME,
            "version": settings.VERSION,
            "debug_mode": settings.DEBUG,
            "supported_platforms": settings.SUPPORTED_PLATFORMS,
            "default_temperatures": settings.DEFAULT_TEMPERATURES,
            "image_generation_enabled": settings.IMAGE_GENERATION_ENABLED,
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        raise HTTPException(status_code=500, detail="시스템 상태 확인 중 오류가 발생했습니다.")