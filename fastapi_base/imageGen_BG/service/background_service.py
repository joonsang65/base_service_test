import time
from PIL import Image
from typing import Tuple, Dict, Any

from ..utils.image_utils import ImageProcessor
from ..schemas.response_schemas import BackgroundRemovalResponse, ProductPositionResponse

class BackgroundService:
    def __init__(self):
        self.image_processor = ImageProcessor()
    
    async def remove_background(
        self, 
        product_image: Image.Image,
        config: Dict[str, Any]
    ) -> BackgroundRemovalResponse:
        """배경 제거 (누끼따기)"""
        start_time = time.time()
        
        try:
            # 배경 제거 실행
            original_img, bg_removed_img = self.image_processor.remove_background(product_image)
            
            # base64 인코딩
            original_b64 = self.image_processor.encode_to_base64(original_img)
            bg_removed_b64 = self.image_processor.encode_to_base64(bg_removed_img)
            
            processing_time = time.time() - start_time
            
            return BackgroundRemovalResponse(
                success=True,
                message="배경 제거 완료",
                original_image=original_b64,
                background_removed_image=bg_removed_b64,
                processing_time=processing_time
            )
            
        except Exception as e:
            return BackgroundRemovalResponse(
                success=False,
                message=f"배경 제거 실패: {str(e)}",
                original_image="",
                background_removed_image="",
                processing_time=time.time() - start_time
            )
    
    async def position_product(
        self,
        product_image: Image.Image,
        canvas_size: Tuple[int, int],
        scale: int,
        position: Tuple[int, int]
    ) -> ProductPositionResponse:
        """제품을 캔버스에 배치"""
        start_time = time.time()
        
        try:
            # 캔버스 생성
            canvas = self.image_processor.create_canvas(canvas_size)
            
            # 제품 크기 조정
            new_size = tuple([int(dim * scale / 100) for dim in product_image.size])
            resized_product = self.image_processor.resize_image(product_image, new_size)
            
            # 제품 배치
            positioned_image = self.image_processor.overlay_product(canvas, resized_product, position)
            
            # 마스크 생성
            mask = self.image_processor.create_mask(positioned_image)
            
            # base64 인코딩
            positioned_b64 = self.image_processor.encode_to_base64(positioned_image)
            mask_b64 = self.image_processor.encode_to_base64(mask)
            
            processing_time = time.time() - start_time
            
            return ProductPositionResponse(
                success=True,
                message="제품 배치 완료",
                positioned_image=positioned_b64,
                mask_image=mask_b64,
                canvas_size=canvas_size,
                position=position,
                processing_time=processing_time
            )
            
        except Exception as e:
            return ProductPositionResponse(
                success=False,
                message=f"제품 배치 실패: {str(e)}",
                positioned_image="",
                mask_image="",
                canvas_size=canvas_size,
                position=position,
                processing_time=time.time() - start_time
            )