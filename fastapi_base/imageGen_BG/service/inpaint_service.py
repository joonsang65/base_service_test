import time
from PIL import Image
from typing import List

from .pipeline_service import PipelineService
from ..utils.image_utils import ImageProcessor
from ..schemas.response_schemas import InpaintResponse

class InpaintService:
    def __init__(self):
        self.pipeline_service = PipelineService()
        self.image_processor = ImageProcessor()
    
    async def run_inpainting(
        self,
        canvas_image: Image.Image,
        mask_image: Image.Image,
        prompt: str,
        category: str = "cosmetics",
        inference_steps: int = 35,
        guidance_scale: float = 7.0,
        num_images: int = 2
    ) -> InpaintResponse:
        """Inpainting 실행"""
        start_time = time.time()
        
        try:
            # Inpaint 파이프라인 로드
            pipe = await self.pipeline_service.get_inpaint_pipeline(category)
            
            # Inpainting 실행
            generated_images = await self.pipeline_service.run_inpainting(
                pipe=pipe,
                image=canvas_image,
                mask=mask_image,
                prompt=prompt,
                inference_steps=inference_steps,
                guidance_scale=guidance_scale,
                num_images=num_images
            )
            
            # base64 인코딩
            encoded_images = [
                self.image_processor.encode_to_base64(img) for img in generated_images
            ]
            
            processing_time = time.time() - start_time
            
            return InpaintResponse(
                success=True,
                message="Inpainting 완료",
                generated_images=encoded_images,
                prompt_used=prompt,
                processing_time=processing_time
            )
            
        except Exception as e:
            return InpaintResponse(
                success=False,
                message=f"Inpainting 실패: {str(e)}",
                generated_images=[],
                prompt_used=prompt,
                processing_time=time.time() - start_time
            )