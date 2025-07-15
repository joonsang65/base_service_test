"""FastAPI 백엔드와의 통신을 담당하는 클라이언트"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, Tuple, List
import base64
from PIL import Image
from io import BytesIO
import json
from core.config import config

class APIClient:
    """FastAPI 백엔드 통신 클라이언트"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.FASTAPI_BASE_URL
        self.session = requests.Session()
        self.session.timeout = 120  # 2분 타임아웃
    
    def _prepare_image_data(self, image: Image.Image) -> bytes:
        """PIL Image를 bytes로 변환"""
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.getvalue()
    
    def _decode_base64_image(self, base64_str: str) -> Image.Image:
        """base64 문자열을 PIL Image로 변환"""
        image_data = base64.b64decode(base64_str)
        return Image.open(BytesIO(image_data))
    
    def _handle_response(self, response: requests.Response, operation: str) -> Optional[Dict]:
        """API 응답 처리"""
        try:
            response.raise_for_status()
            result = response.json()
            
            if result.get('success', False):
                return result
            else:
                st.error(f"{operation} 실패: {result.get('message', '알 수 없는 오류')}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"{operation} API 호출 오류: {str(e)}")
            return None
        except json.JSONDecodeError:
            st.error(f"{operation} 응답 파싱 오류")
            return None
    
    # 배경 제거 API
    def remove_background(self, image: Image.Image, threshold: int = 250) -> Tuple[Optional[Image.Image], Optional[Image.Image]]:
        """배경 제거 API 호출"""
        try:
            files = {'product_image': ('image.png', self._prepare_image_data(image), 'image/png')}
            data = {'threshold': threshold, 'output_format': 'RGBA'}
            
            response = self.session.post(f"{self.base_url}/api/v1/image/remove-background", files=files, data=data)
            result = self._handle_response(response, "배경 제거")
            
            if result:
                original = self._decode_base64_image(result['original_image'])
                bg_removed = self._decode_base64_image(result['background_removed_image'])
                return original, bg_removed
                
            return None, None
            
        except Exception as e:
            st.error(f"배경 제거 중 오류 발생: {str(e)}")
            return None, None
    
    # 제품 배치 API
    def position_product(self, image: Image.Image, canvas_size: Tuple[int, int], 
                        scale: int, position: Tuple[int, int]) -> Optional[Dict]:
        """제품 배치 API 호출"""
        try:
            files = {'background_removed_image': ('image.png', self._prepare_image_data(image), 'image/png')}
            data = {
                'canvas_width': canvas_size[0],
                'canvas_height': canvas_size[1],
                'scale': scale,
                'pos_x': position[0],
                'pos_y': position[1]
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/image/position-product", files=files, data=data)
            result = self._handle_response(response, "제품 배치")
            
            if result:
                return {
                    'positioned_image': self._decode_base64_image(result['positioned_image']),
                    'mask_image': self._decode_base64_image(result['mask_image']),
                    'canvas_size': result['canvas_size'],
                    'position': result['position']
                }
            return None
            
        except Exception as e:
            st.error(f"제품 배치 중 오류 발생: {str(e)}")
            return None
    
    # GPT 광고 분석 API
    def analyze_advertisement(self, product_image: Image.Image, product_type: str = "food",
                            marketing_type: str = "배경 제작", reference_image: Optional[Image.Image] = None) -> Optional[Dict]:
        """GPT 광고 분석 API 호출"""
        try:
            files = {'product_image': ('product.png', self._prepare_image_data(product_image), 'image/png')}
            if reference_image:
                files['reference_image'] = ('reference.png', self._prepare_image_data(reference_image), 'image/png')
            
            data = {'product_type': product_type, 'marketing_type': marketing_type}
            
            response = self.session.post(f"{self.base_url}/api/v1/image/analyze-ad", files=files, data=data)
            result = self._handle_response(response, "광고 분석")
            
            if result:
                return {
                    'ad_plan': result['ad_plan'],
                    'generated_prompt': result['generated_prompt']
                }
            return None
            
        except Exception as e:
            st.error(f"광고 분석 중 오류 발생: {str(e)}")
            return None
    
    # Inpainting 배경 생성 API
    def inpaint_background(self, canvas_image: Image.Image, mask_image: Image.Image,
                          prompt: str, category: str = "cosmetics") -> Optional[List[Image.Image]]:
        """Inpainting 배경 생성 API 호출"""
        try:
            files = {
                'canvas_image': ('canvas.png', self._prepare_image_data(canvas_image), 'image/png'),
                'mask_image': ('mask.png', self._prepare_image_data(mask_image), 'image/png')
            }
            data = {
                'prompt': prompt,
                'category': category,
                'inference_steps': 35,
                'guidance_scale': 7.0,
                'num_images': 2
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/image/inpaint", files=files, data=data)
            result = self._handle_response(response, "Inpaint 배경 생성")
            
            if result:
                return [self._decode_base64_image(img_b64) for img_b64 in result['generated_images']]
            return None
            
        except Exception as e:
            st.error(f"Inpaint 배경 생성 중 오류 발생: {str(e)}")
            return None
    
    # Text2Image 배경 생성 API
    def generate_background(self, prompt: str, canvas_size: Tuple[int, int] = (512, 512),
                           category: str = "cosmetics") -> Optional[List[Image.Image]]:
        """Text2Image 배경 생성 API 호출"""
        try:
            data = {
                'prompt': prompt,
                'canvas_width': canvas_size[0],
                'canvas_height': canvas_size[1],
                'category': category,
                'inference_steps': 35,
                'guidance_scale': 7.0,
                'num_images': 2
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/image/generate-background", data=data)
            result = self._handle_response(response, "배경 생성")
            
            if result:
                return [self._decode_base64_image(img_b64) for img_b64 in result['generated_images']]
            return None
            
        except Exception as e:
            st.error(f"배경 생성 중 오류 발생: {str(e)}")
            return None
    
    # IP-Adapter 스무딩 API
    def apply_smoothing(self, background_image: Image.Image, product_image: Image.Image,
                       prompt: str, category: str = "cosmetics") -> Optional[Image.Image]:
        """IP-Adapter 스무딩 API 호출"""
        try:
            files = {
                'background_image': ('background.png', self._prepare_image_data(background_image), 'image/png'),
                'product_image': ('product.png', self._prepare_image_data(product_image), 'image/png')
            }
            data = {
                'prompt': prompt,
                'category': category,
                'scale': 0.7,
                'inference_steps': 35,
                'guidance_scale': 7.0
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/image/smoothing", files=files, data=data)
            result = self._handle_response(response, "이미지 스무딩")
            
            if result:
                return self._decode_base64_image(result['smoothed_image'])
            return None
            
        except Exception as e:
            st.error(f"이미지 스무딩 중 오류 발생: {str(e)}")
            return None
    
    # 텍스트 생성 API
    def generate_ad_text(self, product_name: str, product_usage: str, 
                        brand_name: str, additional_info: str = "") -> Optional[str]:
        """광고 텍스트 생성 API 호출"""
        try:
            data = {
                'product_name': product_name,
                'product_usage': product_usage,
                'brand_name': brand_name,
                'additional_info': additional_info
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/text/generate", json=data)
            result = self._handle_response(response, "광고 텍스트 생성")
            
            if result:
                return result['generated_text']
            return None
            
        except Exception as e:
            st.error(f"광고 텍스트 생성 중 오류 발생: {str(e)}")
            return None
    
    # 텍스트 이미지 생성 API
    def generate_text_image(self, text: str, font_name: str, font_size: int,
                           text_color: str, stroke_color: str, stroke_width: int) -> Optional[Image.Image]:
        """텍스트 이미지 생성 API 호출"""
        try:
            data = {
                'text': text,
                'font_name': font_name,
                'font_size': font_size,
                'text_color': text_color,
                'stroke_color': stroke_color,
                'stroke_width': stroke_width
            }
            
            response = self.session.post(f"{self.base_url}/api/v1/image-text/generate", json=data)
            result = self._handle_response(response, "텍스트 이미지 생성")
            
            if result:
                return self._decode_base64_image(result['text_image'])
            return None
            
        except Exception as e:
            st.error(f"텍스트 이미지 생성 중 오류 발생: {str(e)}")
            return None

# 싱글톤 인스턴스
@st.cache_resource
def get_api_client() -> APIClient:
    """API 클라이언트 싱글톤 인스턴스 반환"""
    return APIClient()