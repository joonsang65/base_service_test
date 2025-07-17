from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from typing import List, Optional, Literal

from ..schemas.response_schemas import (
    BackgroundRemovalResponse, InpaintResponse, GenerateResponse,
    SmoothingResponse, ErrorResponse
)
from ..service.background_service import BackgroundService
from ..service.inpaint_service import InpaintService
from ..service.generate_service import GenerateService
from ..service.smoothing_service import SmoothingService
from ..utils.image_utils import ImageProcessor, validate_image

router = APIRouter()

# 1. 누끼따기 (배경 제거) 엔드포인트
@router.post("/remove-background", response_model=BackgroundRemovalResponse)
async def remove_background(
    product_image: UploadFile = File(...),
    threshold: int = Form(250),
    output_format: str = Form("RGBA")
):
    """이미지 배경 제거 (누끼따기)"""
    try:
        service = BackgroundService()
        product_img = await validate_image(product_image)
        
        result = await service.remove_background(
            product_image=product_img,
            config={
                "threshold": threshold,
                "output_format": output_format
            }
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/position-product")
async def position_product(
    background_removed_image: UploadFile = File(...),
    canvas_width: int = Form(...),
    canvas_height: int = Form(...),
    scale: int = Form(100),
    pos_x: int = Form(100),
    pos_y: int = Form(100)
):
    """제품을 캔버스에 배치"""
    try:
        service = BackgroundService()
        product_img = await validate_image(background_removed_image)
        
        result = await service.position_product(
            product_image=product_img,
            canvas_size=(canvas_width, canvas_height),
            scale=scale,
            position=(pos_x, pos_y)
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. 배경 생성 엔드포인트들
@router.post("/inpaint", response_model=InpaintResponse)
async def inpaint_background(
    canvas_image: UploadFile = File(...),
    mask_image: UploadFile = File(...),
    prompt: str = Form(...),
    category: str = Form("cosmetics"),
    inference_steps: int = Form(35),
    guidance_scale: float = Form(7.0),
    num_images: int = Form(2)
):
    """Inpainting으로 배경 생성"""
    try:
        service = InpaintService()
        canvas_img = await validate_image(canvas_image)
        mask_img = await validate_image(mask_image)
        
        result = await service.run_inpainting(
            canvas_image=canvas_img,
            mask_image=mask_img,
            prompt=prompt,
            category=category,
            inference_steps=inference_steps,
            guidance_scale=guidance_scale,
            num_images=num_images
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-background", response_model=GenerateResponse)
async def generate_background(
    prompt: str = Form(...),
    canvas_width: int = Form(512),
    canvas_height: int = Form(512),
    category: str = Form("cosmetics"),
    inference_steps: int = Form(35),
    guidance_scale: float = Form(7.0),
    num_images: int = Form(2)
):
    """Text2Image로 배경 생성"""
    try:
        service = GenerateService()
        
        result = await service.generate_background(
            prompt=prompt,
            canvas_size=(canvas_width, canvas_height),
            category=category,
            inference_steps=inference_steps,
            guidance_scale=guidance_scale,
            num_images=num_images
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Smoothing (IP-Adapter) 엔드포인트
@router.post("/smoothing", response_model=SmoothingResponse)
async def apply_smoothing(
    background_image: UploadFile = File(...),
    product_image: UploadFile = File(...),
    prompt: str = Form(...),
    category: str = Form("cosmetics"),
    scale: float = Form(0.7),
    inference_steps: int = Form(35),
    guidance_scale: float = Form(7.0)
):
    """IP-Adapter를 통한 이미지 스무딩"""
    try:
        service = SmoothingService()
        bg_img = await validate_image(background_image)
        prod_img = await validate_image(product_image)
        
        result = await service.apply_smoothing(
            background_image=bg_img,
            product_image=prod_img,
            prompt=prompt,
            category=category,
            scale=scale,
            inference_steps=inference_steps,
            guidance_scale=guidance_scale
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. GPT 분석 엔드포인트
@router.post("/analyze-ad")
async def analyze_advertisement(
    product_image: UploadFile = File(...),
    product_type: str = Form("food"),
    marketing_type: str = Form("배경 제작"),
    reference_image: Optional[UploadFile] = File(None)
):
    try:
        from ..service.gpt_service import GPTService
        service = GPTService()

        # 1. 이미지 로드
        product_pil = await validate_image(product_image)
        print("[DEBUG] product_pil:", product_pil)  # 또는 logger.info
        ref_pil = await validate_image(reference_image) if reference_image else None

        # 2. base64로 인코딩
        processor = ImageProcessor()
        product_b64 = processor.encode_to_base64(product_pil)
        print("[DEBUG] product_b64:", product_b64[:100])
        ref_b64 = processor.encode_to_base64(ref_pil) if ref_pil else None

        # 3. GPT 서비스 호출
        result = await service.analyze_ad_plan(
            product_b64=product_b64,
            ref_b64=ref_b64,
            product_type=product_type,
            marketing_type=marketing_type
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"광고 분석 중 오류 발생: {str(e)}")