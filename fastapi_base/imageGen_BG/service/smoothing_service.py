import time
from PIL import Image

from .pipeline_service import PipelineService
from ..utils.image_utils import ImageProcessor
from ..schemas.response_schemas import SmoothingResponse

class SmoothingService:
    def __init__(self):
        self.pipeline_service = PipelineService()
        self.image_processor = ImageProcessor()
    
    async def apply_smoothing(
        self,
        background_image: Image.Image,
        product_image: Image.Image,
        prompt: str,
        category: str = "cosmetics",
        scale: float = 0.7,
        inference_steps: int = 35,
        guidance_scale: float = 7.0
    ) -> SmoothingResponse:
        """IP-Adapter를 통한 스무딩"""
        start_time = time.time()
        
        try:
            # IP-Adapter 로드
            ip_adapter = await self.pipeline_service.get_ip_adapter(category)
            
            # 스무딩 실행
            smoothed_image = await self.pipeline_service.apply_ip_adapter(
                ip_adapter=ip_adapter,
                background_image=background_image,
                product_image=product_image,
                prompt=prompt,
                scale=scale,
                inference_steps=inference_steps,
                guidance_scale=guidance_scale
            )
            
            # base64 인코딩
            smoothed_b64 = self.image_processor.encode_to_base64(smoothed_image)
            
            processing_time = time.time() - start_time
            
            return SmoothingResponse(
                success=True,
                message="스무딩 완료",
                smoothed_image=smoothed_b64,
                processing_time=processing_time
            )
            
        except Exception as e:
            return SmoothingResponse(
                success=False,
                message=f"스무딩 실패: {str(e)}",
                smoothed_image="",
                processing_time=time.time() - start_time
            )