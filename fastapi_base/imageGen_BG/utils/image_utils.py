from PIL import Image, ImageOps
from fastapi import UploadFile, HTTPException
import io
import base64
from rembg import remove
from typing import Tuple, Optional
import time
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """이미지 처리 유틸리티 클래스"""
    
    def remove_background(self, image: Image.Image) -> Tuple[Image.Image, Image.Image]:
        """배경 제거 (model_dev/modules/utils.py의 remove_background 로직 적용)"""
        try:
            logger.info("Removing background from PIL.Image object")
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            input_data = buffered.getvalue()
            original_image = image.convert("RGBA")

            # rembg로 배경 제거
            output_data = remove(input_data)
            transparent_image = Image.open(io.BytesIO(output_data)).convert("RGBA")

            return original_image, transparent_image

        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            raise
    
    def create_canvas(self, size: Tuple[int, int]) -> Image.Image:
        """캔버스 생성"""
        return Image.new("RGBA", size, (255, 255, 255, 255))
    
    def resize_image(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """이미지 크기 조정 (model_dev/modules/utils.py의 resize_to_ratio 로직)"""
        return image.resize(target_size, Image.LANCZOS)
    
    def overlay_product(self, background: Image.Image, product: Image.Image, position: Tuple[int, int]) -> Image.Image:
        """배경 이미지 위에 제품 이미지 합성 (model_dev/modules/utils.py의 overlay_product 로직)"""
        bg = background.convert("RGBA")
        fg = product.convert("RGBA")
        bg.paste(fg, position, fg)
        return bg
    
    def create_mask(self, product_image: Image.Image, threshold: int = 250) -> Image.Image:
        """마스크 생성 (model_dev/modules/utils.py의 create_mask 로직)"""
        logger.info("Creating mask from alpha channel")

        if product_image.mode != "RGBA":
            logger.warning(f"Image mode is {product_image.mode}, converting to RGBA")
            product_image = product_image.convert("RGBA")

        try:
            alpha = product_image.getchannel("A")
            mask = Image.eval(alpha, lambda a: 255 if a > threshold else 0)
            return mask.convert("L")
        except Exception as e:
            logger.error(f"Failed to create mask: {e}")
            raise
    
    def encode_to_base64(self, image: Image.Image, size: Optional[Tuple[int, int]] = None) -> str:
        """이미지를 base64로 인코딩"""
        try:
            if not isinstance(image, Image.Image):
                raise TypeError(f"Unsupported image type: {type(image)}")

            image = image.convert("RGB")

            if size:
                image.thumbnail(size, Image.Resampling.LANCZOS)
            
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            
            # 🔍 버퍼 저장 이후에 검사
            data = buffered.getvalue()
            if not data:
                logger.error("버퍼가 비어 있음: 이미지 저장 실패")
                raise ValueError("이미지를 버퍼에 저장하지 못했습니다.")
            else: 
                print(f"버퍼 데이터 있음 : {data[:100]}")
            return base64.b64encode(data).decode("utf-8")

        except Exception as e:
            logger.error(f"Failed to encode image: {e}")
            raise


async def validate_image(upload_file: UploadFile) -> Image.Image:
    """업로드된 파일을 검증하고 PIL Image로 변환"""
    if not upload_file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
    
    contents = await upload_file.read()
    try:
        image = Image.open(io.BytesIO(contents))
        return image.convert("RGBA")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 처리 실패: {str(e)}")