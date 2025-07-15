from pydantic import BaseModel
from typing import Optional, Literal, Tuple

# 1. 배경 제거 요청
class BackgroundRemovalRequest(BaseModel):
    threshold: int = 250
    output_format: str = "RGBA"

# 2. Inpaint 요청
class InpaintRequest(BaseModel):
    category: str = "cosmetics"
    inference_steps: int = 35
    guidance_scale: float = 7.0
    num_images: int = 2

# 3. Generate 요청  
class GenerateRequest(BaseModel):
    canvas_size: Tuple[int, int] = (512, 512)
    category: str = "cosmetics"
    inference_steps: int = 35
    guidance_scale: float = 7.0
    num_images: int = 2

# 4. Smoothing 요청
class SmoothingRequest(BaseModel):
    category: str = "cosmetics"
    scale: float = 0.7
    inference_steps: int = 35
    guidance_scale: float = 7.0

# 5. 제품 배치 요청
class ProductPositionRequest(BaseModel):
    canvas_size: Tuple[int, int] = (512, 512)
    scale: int = 100  # 10-200
    pos_x: int = 100
    pos_y: int = 100

# 6. GPT 분석 요청
class GPTAnalysisRequest(BaseModel):
    product_type: str = "food"
    marketing_type: str = "배경 제작"