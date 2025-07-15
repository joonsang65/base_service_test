import time
import logging
from typing import Dict, Any, List, Optional
from textGen.models.models import OpenAIClient
from textGen.core.config import settings

logger = logging.getLogger(__name__)

class AdGenerationService:
    """광고 문구 생성 서비스"""
    
    def __init__(self):
        self.openai_client = None
    
    def _get_client(self) -> OpenAIClient:
        """OpenAI 클라이언트 인스턴스 반환 (지연 초기화)"""
        if self.openai_client is None:
            self.openai_client = OpenAIClient()
        return self.openai_client
    
    async def generate_ad_texts(
        self,
        ad_type: str,
        mode_input: str = None,
        product_name: str = "",
        product_use: str = "",
        brand_name: str = "",
        extra_info: str = None
    ):
        """
        광고 문구 생성 요청 함수 (기존 main.py에서 이동)
        """
        openai_client = self._get_client()

        # 모드 결정
        if ad_type in ["인스타그램", "블로그"]:
            if mode_input not in ["1", "2"]:
                raise ValueError("인스타그램 또는 블로그 광고는 mode_input을 '1' 또는 '2'로 지정해야 합니다.")
            mode = "광고 문구만 생성" if mode_input == "1" else "광고 문구 + 텍스트 이미지용 문구 생성"
        else:
            mode = "광고 문구만 생성"

        platforms = [ad_type]

        results = await openai_client.generate_multiple_responses(
            platforms,
            product_name,
            product_use,
            brand_name,
            extra_info,
            mode
        )

        return results
    
    async def generate_single_ad(
        self,
        ad_type: str,
        mode_input: Optional[str],
        product_name: str,
        product_use: str,
        brand_name: str,
        extra_info: Optional[str] = None
    ) -> Dict[str, Any]:
        """단일 플랫폼 광고 문구 생성"""
        start_time = time.time()
        
        try:
            logger.info(f"단일 광고 생성 시작: {ad_type}, {product_name}")
            
            results = await self.generate_ad_texts(
                ad_type=ad_type,
                mode_input=mode_input,
                product_name=product_name,
                product_use=product_use,
                brand_name=brand_name,
                extra_info=extra_info
            )
            
            execution_time = time.time() - start_time
            logger.info(f"단일 광고 생성 완료: {execution_time:.2f}초")
            
            return {
                "results": results,
                "execution_time": execution_time,
                "platform": ad_type,
                "mode": mode_input
            }
            
        except Exception as e:
            logger.error(f"단일 광고 생성 실패: {e}")
            raise
    
    async def generate_multiple_ads(
        self,
        platforms: List[str],
        product_name: str,
        product_use: str,
        brand_name: str,
        extra_info: Optional[str] = None,
        mode: str = "광고 문구만 생성",
        temperatures: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """여러 플랫폼 및 온도 조합으로 광고 문구 생성"""
        start_time = time.time()
        
        try:
            logger.info(f"다중 광고 생성 시작: {platforms}, {product_name}")
            
            client = self._get_client()
            results = await client.generate_multiple_responses(
                platforms=platforms,
                product_name=product_name,
                product_use=product_use,
                brand_name=brand_name,
                extra_info=extra_info,
                mode=mode,
                temperatures=temperatures
            )
            
            execution_time = time.time() - start_time
            logger.info(f"다중 광고 생성 완료: {execution_time:.2f}초")
            
            return {
                "results": results,
                "execution_time": execution_time,
                "platforms": platforms,
                "mode": mode,
                "temperatures": temperatures or settings.DEFAULT_TEMPERATURES
            }
            
        except Exception as e:
            logger.error(f"다중 광고 생성 실패: {e}")
            raise
    
    async def generate_single_temperature_ads(
        self,
        platforms: List[str],
        product_name: str,
        product_use: str,
        brand_name: str,
        extra_info: Optional[str] = None,
        mode: str = "광고 문구만 생성"
    ) -> Dict[str, Any]:
        """단일 온도로 여러 플랫폼 광고 문구 생성"""
        start_time = time.time()
        
        try:
            logger.info(f"단일 온도 다중 플랫폼 광고 생성 시작: {platforms}, {product_name}")
            
            client = self._get_client()
            results = await client.generate_texts(
                platforms=platforms,
                product_name=product_name,
                product_use=product_use,
                brand_name=brand_name,
                extra_info=extra_info,
                mode=mode
            )
            
            execution_time = time.time() - start_time
            logger.info(f"단일 온도 다중 플랫폼 광고 생성 완료: {execution_time:.2f}초")
            
            return {
                "results": results,
                "execution_time": execution_time,
                "platforms": platforms,
                "mode": mode,
                "temperature": 0.7  # 기본값
            }
            
        except Exception as e:
            logger.error(f"단일 온도 다중 플랫폼 광고 생성 실패: {e}")
            raise
        
# 서비스 인스턴스 생성
ad_service = AdGenerationService()
