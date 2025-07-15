from fastapi import APIRouter, HTTPException
import logging
from textGen.schemas.textGen_schemas import (
    SingleAdRequest, 
    MultiPlatformRequest, 
    SingleTemperatureRequest,
    AdGenerationResponse,

)
from textGen.service.textGen_service import ad_service
from textGen.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/textGen-multiTP_singlePF", response_model=AdGenerationResponse)
async def generate_single_ad(request: SingleAdRequest):
    """
    단일 플랫폼 광고 문구 생성
    
    - **ad_type**: 광고 유형 (인스타그램, 블로그, 포스터)
    - **mode_input**: 모드 선택 (1: 광고 문구만, 2: 광고 문구 + 텍스트 이미지용)
    - **product_name**: 상품 이름
    - **product_use**: 상품 용도
    - **brand_name**: 브랜드명
    - **extra_info**: 추가 정보 (선택사항)
    """
    try:
        logger.info(f"단일 광고 생성 요청: {request.ad_type} - {request.product_name}")
        
        result = await ad_service.generate_single_ad(
            ad_type=request.ad_type,
            mode_input=request.mode_input,
            product_name=request.product_name,
            product_use=request.product_use,
            brand_name=request.brand_name,
            extra_info=request.extra_info
        )
        
        return AdGenerationResponse(
            success=True,
            data=result,
            message=f"{request.ad_type} 광고 문구가 성공적으로 생성되었습니다.",
            execution_time=result.get("execution_time")
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ad generation failed: {e}")
        raise HTTPException(status_code=500, detail="광고 문구 생성 중 오류가 발생했습니다.")

@router.post("/textGen_multiTP_multiPF", response_model=AdGenerationResponse)
async def generate_multiple_ads(request: MultiPlatformRequest):
    """
    여러 플랫폼 및 온도 조합으로 광고 문구 생성
    
    - **platforms**: 대상 플랫폼 리스트
    - **product_name**: 상품 이름
    - **product_use**: 상품 용도
    - **brand_name**: 브랜드명
    - **extra_info**: 추가 정보 (선택사항)
    - **mode**: 생성 모드
    - **temperatures**: 온도 값 리스트 (선택사항)
    """
    try:
        logger.info(f"다중 광고 생성 요청: {request.platforms} - {request.product_name}")
        
        result = await ad_service.generate_multiple_ads(
            platforms=request.platforms,
            product_name=request.product_name,
            product_use=request.product_use,
            brand_name=request.brand_name,
            extra_info=request.extra_info,
            mode=request.mode,
            temperatures=request.temperatures
        )
        
        return AdGenerationResponse(
            success=True,
            data=result,
            message=f"{len(request.platforms)}개 플랫폼 광고 문구가 성공적으로 생성되었습니다.",
            execution_time=result.get("execution_time")
        )
        
    except Exception as e:
        logger.error(f"Multiple ads generation failed: {e}")
        raise HTTPException(status_code=500, detail="광고 문구 생성 중 오류가 발생했습니다.")

@router.post("/signleTP_multiPF", response_model=AdGenerationResponse)
async def generate_single_temperature_ads(request: SingleTemperatureRequest):
    """
    단일 온도로 여러 플랫폼 광고 문구 생성
    
    - **platforms**: 대상 플랫폼 리스트
    - **product_name**: 상품 이름
    - **product_use**: 상품 용도
    - **brand_name**: 브랜드명
    - **extra_info**: 추가 정보 (선택사항)
    - **mode**: 생성 모드
    """
    try:
        logger.info(f"단일 온도 다중 플랫폼 광고 생성 요청: {request.platforms} - {request.product_name}")
        
        result = await ad_service.generate_single_temperature_ads(
            platforms=request.platforms,
            product_name=request.product_name,
            product_use=request.product_use,
            brand_name=request.brand_name,
            extra_info=request.extra_info,
            mode=request.mode
        )
        
        return AdGenerationResponse(
            success=True,
            data=result,
            message=f"{len(request.platforms)}개 플랫폼 단일 온도 광고 문구가 성공적으로 생성되었습니다.",
            execution_time=result.get("execution_time")
        )
        
    except Exception as e:
        logger.error(f"Single temperature ads generation failed: {e}")
        raise HTTPException(status_code=500, detail="광고 문구 생성 중 오류가 발생했습니다.")