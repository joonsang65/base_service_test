from typing import Optional
import os
import httpx
from openai import AsyncOpenAI, OpenAIError
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class GPTService:
    def __init__(self):
        transport = httpx.AsyncHTTPTransport(proxy=None)

        self.client = AsyncOpenAI(
            api_key=os.getenv(settings.config['openai']['api_key_env']),
            http_client=httpx.AsyncClient(transport=transport)
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
        try:
            messages = [
                {
                    "role": "system",
                    "content": "당신은 광고 기획 전문가입니다."
                },
                {
                    "role": "user",
                    "content": (
                        f"제품 이미지(base64): {product_b64[:50]}...\n"
                        f"참고 이미지(base64): {ref_b64[:50] if ref_b64 else '없음'}\n"
                        f"제품 유형: {product_type}\n"
                        f"마케팅 유형: {marketing_type}\n"
                        "이 정보를 바탕으로 광고 기획안을 작성해주세요."
                    )
                }
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            content = response.choices[0].message.content
            return content

        except OpenAIError as e:
            logger.error(f"OpenAI API 호출 실패: {e}")
            raise RuntimeError(f"OpenAI API 호출 실패: {e}")

        except Exception as e:
            logger.error(f"광고 기획 분석 중 오류 발생: {e}")
            raise RuntimeError(f"광고 기획 분석 중 오류 발생: {e}")

    async def convert_to_sd_prompt(self, ad_description: str) -> str:
        """광고 기획을 Stable Diffusion 프롬프트로 변환"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "당신은 Stable Diffusion 프롬프트 전문가입니다."
                },
                {
                    "role": "user",
                    "content": f"다음 광고 기획을 Stable Diffusion 프롬프트로 변환해 주세요:\n{ad_description}"
                }
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,
                max_tokens=200,
            )
            content = response.choices[0].message.content
            return content

        except OpenAIError as e:
            logger.error(f"OpenAI API 호출 실패: {e}")
            raise RuntimeError(f"OpenAI API 호출 실패: {e}")

        except Exception as e:
            logger.error(f"SD 프롬프트 변환 중 오류 발생: {e}")
            raise RuntimeError(f"SD 프롬프트 변환 중 오류 발생: {e}")
