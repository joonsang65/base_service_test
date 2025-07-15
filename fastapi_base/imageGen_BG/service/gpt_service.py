from openai import AsyncOpenAI
from typing import Optional
import os
from ..core.config import settings

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv(settings.config['openai']['api_key_env'])
        )
        self.model = settings.config['openai']['gpt_model']
    
    async def analyze_ad_plan(
        self,
        product_b64: str,
        ref_b64: Optional[str],
        product_type: str,
        marketing_type: str
    ) -> str:
        """광고 기획안 생성"""
        # GPT 모듈의 analyze_ad_plan 로직을 async로 변환
        pass
    
    async def convert_to_sd_prompt(self, ad_description: str) -> str:
        """광고 기획을 SD 프롬프트로 변환"""
        # GPT 모듈의 convert_to_sd_prompt 로직을 async로 변환
        pass