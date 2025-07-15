"""FastAPI 메인 애플리케이션"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
from rembg import remove
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# GPT 서비스 import
from textGen.service.gpt_text_service import GPTTextService
from imageGen_BG.service.background_service import BackgroundService
from imageGen_BG.service.inpaint_service import InpaintService
from imageGen_Text.service.text_image_service import TextImageService

app = FastAPI(title="AI 광고 제작 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 인스턴스 생성
gpt_service = GPTTextService()
background_service = BackgroundService()
inpaint_service = InpaintService()
text_image_service = TextImageService()

def image_to_base64(image: Image.Image) -> str:
    """이미지를 base64로 변환"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def base64_to_image(base64_str: str) -> Image.Image:
    """base64를 이미지로 변환"""
    image_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(image_data))

@app.get("/")
async def root():
    return {"message": "AI 광고 제작 API 실행 중"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/image/remove-background")
async def remove_background_api(
    product_image: UploadFile = File(...),
    threshold: int = Form(250),
    output_format: str = Form("RGBA")
):
    """실제 배경 제거 기능"""
    try:
        # 이미지 로드
        image_data = await product_image.read()
        original_image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        
        # BackgroundService 사용
        result = await background_service.remove_background(original_image, {"threshold": threshold})
        
        if result.success:
            return {
                "success": True,
                "message": "배경 제거 완료",
                "original_image": result.original_image,
                "background_removed_image": result.background_removed_image,
                "processing_time": result.processing_time
            }
        else:
            # BackgroundService 실패 시 rembg 직접 사용
            removed_bg_data = remove(image_data)
            bg_removed_image = Image.open(io.BytesIO(removed_bg_data)).convert("RGBA")
            
            return {
                "success": True,
                "message": "배경 제거 완료 (rembg)",
                "original_image": image_to_base64(original_image),
                "background_removed_image": image_to_base64(bg_removed_image),
                "processing_time": 1.5
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"배경 제거 실패: {str(e)}",
            "original_image": "",
            "background_removed_image": "",
            "processing_time": 0.0
        }

@app.post("/api/v1/image/position-product")
async def position_product_api(
    background_removed_image: UploadFile = File(...),
    canvas_width: int = Form(...),
    canvas_height: int = Form(...),
    scale: int = Form(100),
    pos_x: int = Form(100),
    pos_y: int = Form(100)
):
    """실제 제품 배치 기능"""
    try:
        # 이미지 로드
        image_data = await background_removed_image.read()
        product_image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        
        # BackgroundService 사용
        result = await background_service.position_product(
            image=product_image,
            canvas_size=(canvas_width, canvas_height),
            scale=scale,
            position=(pos_x, pos_y)
        )
        
        if result.success:
            return {
                "success": True,
                "message": "제품 배치 완료",
                "positioned_image": result.positioned_image,
                "mask_image": result.mask_image,
                "canvas_size": result.canvas_size,
                "position": result.position,
                "processing_time": result.processing_time
            }
        else:
            raise Exception(result.message)
            
    except Exception as e:
        return {
            "success": False,
            "message": f"제품 배치 실패: {str(e)}",
            "positioned_image": "",
            "mask_image": "",
            "processing_time": 0.0
        }

@app.post("/api/v1/image/analyze-ad")
async def analyze_advertisement_api(
    product_image: UploadFile = File(...),
    product_type: str = Form("food"),
    marketing_type: str = Form("배경 제작"),
    reference_image: UploadFile = File(None)
):
    """GPT를 통한 광고 분석"""
    try:
        # 이미지 로드 및 base64 변환
        product_data = await product_image.read()
        product_img = Image.open(io.BytesIO(product_data))
        product_b64 = image_to_base64(product_img)
        
        ref_b64 = None
        if reference_image:
            ref_data = await reference_image.read()
            ref_img = Image.open(io.BytesIO(ref_data))
            ref_b64 = image_to_base64(ref_img)
        
        # GPT 서비스 사용
        ad_plan = await gpt_service.analyze_ad_plan(
            product_b64=product_b64,
            ref_b64=ref_b64,
            product_type=product_type,
            marketing_type=marketing_type
        )
        
        generated_prompt = await gpt_service.convert_to_sd_prompt(ad_plan)
        
        return {
            "success": True,
            "message": "광고 분석 완료",
            "ad_plan": ad_plan,
            "generated_prompt": generated_prompt,
            "processing_time": 3.0
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"광고 분석 실패: {str(e)}",
            "ad_plan": "",
            "generated_prompt": "",
            "processing_time": 0.0
        }

@app.post("/api/v1/text/generate")
async def generate_text_api(
    product_name: str = Form(...),
    product_usage: str = Form(...),
    brand_name: str = Form(...),
    additional_info: str = Form("")
):
    """실제 GPT 텍스트 생성 기능"""
    try:
        # GPT 서비스 사용
        generated_text = await gpt_service.generate_ad_text(
            product_name=product_name,
            product_usage=product_usage,
            brand_name=brand_name,
            additional_info=additional_info
        )
        
        if generated_text:
            return {
                "success": True,
                "message": "텍스트 생성 완료",
                "generated_text": generated_text,
                "processing_time": 2.0
            }
        else:
            # GPT 실패 시 템플릿 사용
            templates = [
                f"✨ {brand_name}의 {product_name}로 {product_usage}를 더 특별하게!",
                f"🌟 {product_name} - {brand_name}만의 품질을 경험하세요",
                f"💎 프리미엄 {product_name}으로 당신의 {product_usage}를 완성하세요"
            ]
            import random
            fallback_text = random.choice(templates)
            
            return {
                "success": True,
                "message": "텍스트 생성 완료 (템플릿)",
                "generated_text": fallback_text,
                "processing_time": 0.5
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"텍스트 생성 실패: {str(e)}",
            "generated_text": "",
            "processing_time": 0.0
        }

@app.post("/api/v1/image-text/generate")
async def generate_text_image_api(
    text: str = Form(...),
    font_name: str = Form("Noto Sans KR"),
    font_size: int = Form(80),
    text_color: str = Form("#000000"),
    stroke_color: str = Form("#FFFFFF"),
    stroke_width: int = Form(2)
):
    """텍스트 이미지 생성"""
    try:
        # TextImageService 사용
        text_image = await text_image_service.create_text_image(
            text=text,
            font_name=font_name,
            font_size=font_size,
            text_color=text_color,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )
        
        if text_image:
            return {
                "success": True,
                "message": "텍스트 이미지 생성 완료",
                "text_image": image_to_base64(text_image),
                "processing_time": 1.0
            }
        else:
            raise Exception("텍스트 이미지 생성 실패")
            
    except Exception as e:
        return {
            "success": False,
            "message": f"텍스트 이미지 생성 실패: {str(e)}",
            "text_image": "",
            "processing_time": 0.0
        }

@app.post("/api/v1/image/inpaint")
async def inpaint_background_api(
    canvas_image: UploadFile = File(...),
    mask_image: UploadFile = File(...),
    prompt: str = Form(...),
    category: str = Form("cosmetics"),
    inference_steps: int = Form(35),
    guidance_scale: float = Form(7.0),
    num_images: int = Form(2)
):
    """Inpainting 배경 생성"""
    try:
        # 이미지 로드
        canvas_data = await canvas_image.read()
        mask_data = await mask_image.read()
        
        canvas_img = Image.open(io.BytesIO(canvas_data))
        mask_img = Image.open(io.BytesIO(mask_data))
        
        # InpaintService 사용
        result = await inpaint_service.run_inpainting(
            canvas_image=canvas_img,
            mask_image=mask_img,
            prompt=prompt,
            category=category,
            inference_steps=inference_steps,
            guidance_scale=guidance_scale,
            num_images=num_images
        )
        
        if result.success:
            return {
                "success": True,
                "message": "Inpainting 완료",
                "generated_images": result.generated_images,
                "prompt_used": result.prompt_used,
                "processing_time": result.processing_time
            }
        else:
            raise Exception(result.message)
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Inpainting 실패: {str(e)}",
            "generated_images": [],
            "prompt_used": prompt,
            "processing_time": 0.0
        }

@app.post("/api/v1/image/generate-background")
async def generate_background_api(
    prompt: str = Form(...),
    canvas_width: int = Form(512),
    canvas_height: int = Form(512),
    category: str = Form("cosmetics"),
    inference_steps: int = Form(35),
    guidance_scale: float = Form(7.0),
    num_images: int = Form(2)
):
    """Text2Image 배경 생성"""
    try:
        from imageGen_BG.service.generate_service import GenerateService
        generate_service = GenerateService()
        
        result = await generate_service.generate_background(
            prompt=prompt,
            canvas_size=(canvas_width, canvas_height),
            category=category,
            inference_steps=inference_steps,
            guidance_scale=guidance_scale,
            num_images=num_images
        )
        
        if result.success:
            return {
                "success": True,
                "message": "배경 생성 완료",
                "generated_images": result.generated_images,
                "prompt_used": result.prompt_used,
                "processing_time": result.processing_time
            }
        else:
            raise Exception(result.message)
            
    except Exception as e:
        return {
            "success": False,
            "message": f"배경 생성 실패: {str(e)}",
            "generated_images": [],
            "prompt_used": prompt,
            "processing_time": 0.0
        }