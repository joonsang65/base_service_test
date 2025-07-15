import time
from PIL import Image
from typing import List, Tuple

from .pipeline_service import PipelineService
from ..utils.image_utils import ImageProcessor
from ..schemas.response_schemas import GenerateResponse

class GenerateService:
    def __init__(self):
        self.pipeline_service = PipelineService()
        self.image_processor = ImageProcessor()
    
    async def generate_background(
        self,
        prompt: str,
        canvas_size: Tuple[int, int] = (512, 512),
        category: str = "cosmetics",
        inference_steps: int = 35,
        guidance_scale: float = 7.0,
        num_images: int = 2
    ) -> GenerateResponse:
        """Text2Image로 배경 생성"""
        start_time = time.time()
        
        try:
            # Text2Image 파이프라인 로드
            pipe = await self.pipeline_service.get_text2img_pipeline(category)
            
            # 배경 생성
            generated_images = await self.pipeline_service.generate_background(
                pipe=pipe,
                prompt=prompt,
                canvas_size=canvas_size,
                inference_steps=inference_steps,
                guidance_scale=guidance_scale,
                num_images=num_images
            )
            
            # base64 인코딩
            encoded_images = [
                self.image_processor.encode_to_base64(img) for img in generated_images
            ]
            
            processing_time = time.time() - start_time
            
            return GenerateResponse(
                success=True,
                message="배경 생성 완료",
                generated_images=encoded_images,
                prompt_used=prompt,
                processing_time=processing_time
            )
            
        except Exception as e:
            return GenerateResponse(
                success=False,
                message=f"배경 생성 실패: {str(e)}",
                generated_images=[],
                prompt_used=prompt,
                processing_time=time.time() - start_time
            )