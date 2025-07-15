"""홈 페이지"""
import streamlit as st
from pathlib import Path
from core.config import config
from utils.styles import CARD_CSS
from utils.helpers import get_base64_image

def render():
    """홈 페이지 렌더링"""
    st.markdown(CARD_CSS, unsafe_allow_html=True)
    
    # 헤더
    st.title("🎨 AI 광고 제작 플랫폼")
    st.markdown("### 원하는 플랫폼에 맞는 광고를 AI로 쉽게 만들어보세요!")
    
    st.markdown("---")
    
    # 플랫폼별 예시 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_platform_card(
            "인스타그램",
            "instagram_example.png",
            "정사각형 비율의 인스타그램 피드용 광고",
            "📸",
            "#E1306C"
        )
    
    with col2:
        render_platform_card(
            "블로그",
            "blog_example.png", 
            "가로형 비율의 블로그 포스트용 광고",
            "📝",
            "#FF6B35"
        )
    
    with col3:
        render_platform_card(
            "포스터",
            "poster_example.png",
            "세로형 비율의 인쇄용 포스터 광고",
            "🖼️",
            "#4A90E2"
        )
    
    # 사용 방법 안내
    st.markdown("---")
    render_how_to_use()
    
    # 특징 소개
    st.markdown("---")
    render_features()

def render_platform_card(title, image_name, description, icon, color):
    """플랫폼 카드 렌더링"""
    image_path = config.get_image_path() / "examples" / image_name
    
    # 기본 이미지가 없을 경우 플레이스홀더 사용
    if image_path.exists():
        img_data = get_base64_image(image_path)
    else:
        # 플레이스홀더 이미지 생성
        img_data = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='300' height='200' viewBox='0 0 300 200'%3e%3crect width='300' height='200' fill='%23f8f9fa'/%3e%3ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='%236c757d'%3e예시 이미지%3c/text%3e%3c/svg%3e"
    
    card_html = f"""
    <div class="ad-card" style="border-left: 4px solid {color};">
        <h4>{icon} {title} 광고</h4>
        <img src="{img_data}" alt="{title} 예시" />
        <p>{description}</p>
        <div class="cta">👆 사이드바에서 '{title}'을 선택하여 시작하세요!</div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_how_to_use():
    """사용 방법 안내"""
    st.markdown("## 🚀 사용 방법")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 1️⃣ 제품 이미지
        - 제품 사진 업로드
        - AI 자동 배경 제거
        - 위치 및 크기 조정
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ 배경 생성
        - GPT가 상황 분석
        - AI로 배경 이미지 생성
        - 자연스러운 합성
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ 텍스트 생성
        - 제품 정보 입력
        - AI 광고 문구 생성
        - 폰트 및 색상 설정
        """)
    
    with col4:
        st.markdown("""
        ### 4️⃣ 최종 완성
        - 텍스트 위치 조정
        - 실시간 미리보기
        - 고품질 이미지 다운로드
        """)

def render_features():
    """특징 소개"""
    st.markdown("## ✨ 주요 특징")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🤖 AI 기반 자동화
        - **배경 제거**: 자동으로 제품 배경 제거
        - **텍스트 생성**: GPT가 매력적인 광고 문구 작성
        - **이미지 합성**: AI가 자연스럽게 이미지 합성
        
        ### 🎨 전문가 수준 디자인
        - **다양한 폰트**: 한글 및 영문 폰트 지원
        - **실시간 미리보기**: 즉시 결과 확인
        - **고해상도 출력**: 인쇄 가능한 품질
        """)
    
    with col2:
        st.markdown("""
        ### 📱 플랫폼 최적화
        - **인스타그램**: 1:1 정사각형 비율
        - **블로그**: 4:3 가로형 비율  
        - **포스터**: 3:4 세로형 비율
        
        ### ⚡ 빠르고 간편
        - **4단계 완성**: 5분 내 광고 제작
        - **즉시 다운로드**: 완성과 동시에 사용
        - **무제한 수정**: 원하는 만큼 재생성
        """)
    
    # CTA 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 지금 시작하기", type="primary", use_container_width=True):
            st.info("👈 사이드바에서 '광고 생성'을 선택하고 플랫폼을 골라주세요!")