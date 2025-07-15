from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, List, Dict, Any
from textGen.core.config import settings

class BaseAdRequest(BaseModel):
    """광고 요청 기본 스키마"""
    product_name: str = Field(..., description="상품 이름", example="프리미엄 스킨케어 세트")
    product_use: str = Field(..., description="상품 용도", example="피부 보습 및 안티에이징")
    brand_name: str = Field(..., description="브랜드명", example="뷰티랩")
    extra_info: Optional[str] = Field(None, description="추가 정보", example="천연 성분 사용, 모든 피부 타입에 적합")

class SingleAdRequest(BaseAdRequest):
    """단일 플랫폼 광고 문구 생성 요청"""
    ad_type: str = Field(..., description="광고 유형 (인스타그램, 블로그, 포스터)", example="인스타그램")
    mode_input: Optional[str] = Field(None, description="모드 선택 - 1: 광고 문구만, 2: 광고 문구 + 텍스트 이미지용 (포스터는 None)", example="1")
    
    @field_validator('ad_type')
    @classmethod
    def validate_ad_type(cls, v: str) -> str:
        if v not in settings.SUPPORTED_PLATFORMS:
            raise ValueError(f'지원되지 않는 광고 유형입니다. 사용 가능한 유형: {settings.SUPPORTED_PLATFORMS}')
        return v
    
    @field_validator('mode_input')
    @classmethod
    def validate_mode_input(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data and 'ad_type' in info.data:
            ad_type = info.data['ad_type']
            if ad_type in ["인스타그램", "블로그"] and v not in ["1", "2"]:
                raise ValueError('인스타그램 또는 블로그 광고는 mode_input을 "1" 또는 "2"로 지정해야 합니다.')
        return v

class MultiPlatformRequest(BaseAdRequest):
    """여러 플랫폼 광고 문구 생성 요청"""
    platforms: List[str] = Field(..., description="대상 플랫폼 리스트", example=["인스타그램", "블로그"])
    mode: str = Field("광고 문구만 생성", description="생성 모드")
    temperatures: Optional[List[float]] = Field(None, description="온도 값 리스트", example=[0.3, 0.7, 1.0])
    
    @field_validator('platforms')
    @classmethod
    def validate_platforms(cls, v: List[str]) -> List[str]:
        invalid_platforms = [p for p in v if p not in settings.SUPPORTED_PLATFORMS]
        if invalid_platforms:
            raise ValueError(f'지원되지 않는 플랫폼: {invalid_platforms}. 사용 가능한 플랫폼: {settings.SUPPORTED_PLATFORMS}')
        return v
    
    @field_validator('temperatures')
    @classmethod
    def validate_temperatures(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        if v is not None:
            for temp in v:
                if not 0 <= temp <= 2:
                    raise ValueError('온도 값은 0과 2 사이여야 합니다.')
        return v

class SingleTemperatureRequest(BaseAdRequest):
    """단일 온도 광고 문구 생성 요청"""
    platforms: List[str] = Field(..., description="대상 플랫폼 리스트", example=["인스타그램"])
    mode: str = Field("광고 문구만 생성", description="생성 모드")
    
    @field_validator('platforms')
    @classmethod
    def validate_platforms(cls, v: List[str]) -> List[str]:
        invalid_platforms = [p for p in v if p not in settings.SUPPORTED_PLATFORMS]
        if invalid_platforms:
            raise ValueError(f'지원되지 않는 플랫폼: {invalid_platforms}. 사용 가능한 플랫폼: {settings.SUPPORTED_PLATFORMS}')
        return v

# 이미지 생성 관련 스키마 (추후 확장용)
class ImageGenerationRequest(BaseModel):
    """이미지 생성 요청 (추후 구현 예정)"""
    prompt: str = Field(..., description="이미지 생성 프롬프트")
    style: Optional[str] = Field("realistic", description="이미지 스타일")
    size: Optional[str] = Field("1024x1024", description="이미지 크기")
    
    @field_validator('size')
    @classmethod
    def validate_size(cls, v: str) -> str:
        valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
        if v not in valid_sizes:
            raise ValueError(f'지원되지 않는 이미지 크기입니다. 사용 가능한 크기: {valid_sizes}')
        return v
    
class AdWithImageRequest(BaseAdRequest):
    """광고 문구 + 이미지 생성 요청 (추후 구현 예정)"""
    ad_type: str = Field(..., description="광고 유형")
    include_image: bool = Field(True, description="이미지 생성 포함 여부")
    image_style: Optional[str] = Field("modern", description="이미지 스타일")
    
    @field_validator('ad_type')
    @classmethod
    def validate_ad_type(cls, v: str) -> str:
        if v not in settings.SUPPORTED_PLATFORMS:
            raise ValueError(f'지원되지 않는 광고 유형입니다. 사용 가능한 유형: {settings.SUPPORTED_PLATFORMS}')
        return v

# 응답 스키마
class AdGenerationResponse(BaseModel):
    """광고 문구 생성 응답"""
    success: bool = Field(..., description="성공 여부")
    data: Dict[str, Any] = Field(..., description="생성된 광고 문구 데이터")
    message: str = Field(..., description="응답 메시지")
    execution_time: Optional[float] = Field(None, description="실행 시간(초)")

class ImageGenerationResponse(BaseModel):
    """이미지 생성 응답 (추후 구현 예정)"""
    success: bool = Field(..., description="성공 여부")
    image_url: Optional[str] = Field(None, description="생성된 이미지 URL")
    message: str = Field(..., description="응답 메시지")

class HealthResponse(BaseModel):
    """헬스 체크 응답"""
    status: str = Field(..., description="서비스 상태")
    message: str = Field(..., description="상태 메시지")
    timestamp: Optional[str] = Field(None, description="체크 시간")
    available_services: List[str] = Field(..., description="사용 가능한 서비스 목록")

class ErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = Field(False, description="성공 여부")
    error: str = Field(..., description="에러 메시지")
    error_code: Optional[str] = Field(None, description="에러 코드")

class PlatformInfo(BaseModel):
    """플랫폼 정보"""
    platforms: List[str] = Field(..., description="지원되는 플랫폼 목록")
    modes: Dict[str, List[Optional[str]]] = Field(..., description="플랫폼별 모드")
    mode_descriptions: Dict[str, str] = Field(..., description="모드 설명")
    default_temperatures: List[float] = Field(..., description="기본 온도 값들")
    image_generation_enabled: bool = Field(..., description="이미지 생성 기능 활성화 여부")