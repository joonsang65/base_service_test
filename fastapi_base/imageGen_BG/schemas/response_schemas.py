from pydantic import BaseModel
from typing import List, Optional

# 1. 배경 제거 응답
class BackgroundRemovalResponse(BaseModel):
    success: bool
    message: str
    original_image: str  # base64
    background_removed_image: str  # base64
    processing_time: float

# 2. 제품 배치 응답
class ProductPositionResponse(BaseModel):
    success: bool
    message: str
    positioned_image: str  # base64
    mask_image: str  # base64
    canvas_size: tuple
    position: tuple
    processing_time: float

# 3. Inpaint 응답
class InpaintResponse(BaseModel):
    success: bool
    message: str
    generated_images: List[str]  # base64 인코딩된 이미지들
    prompt_used: str
    processing_time: float

# 4. Generate 응답
class GenerateResponse(BaseModel):
    success: bool
    message: str
    generated_images: List[str]  # base64 인코딩된 이미지들
    prompt_used: str
    processing_time: float

# 5. Smoothing 응답
class SmoothingResponse(BaseModel):
    success: bool
    message: str
    smoothed_image: str  # base64
    processing_time: float

# 6. GPT 분석 응답
class GPTAnalysisResponse(BaseModel):
    success: bool
    message: str
    ad_plan: str
    generated_prompt: str
    processing_time: float

# 공통 에러 응답
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None