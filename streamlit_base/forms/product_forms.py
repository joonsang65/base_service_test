"""제품 정보 입력 폼"""
import streamlit as st
from core.session_manager import SessionManager

def render_product_info_form(api_client):
    """제품 정보 입력 폼 렌더링"""
    
    with st.form("product_info_form", clear_on_submit=False):
        st.markdown("#### 📦 기본 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.text_input(
                "제품명",
                value=SessionManager.get("product_name", ""),
                placeholder="예: 프리미엄 오가닉 사과",
                help="판매하는 제품의 정확한 이름을 입력하세요"
            )
            
            brand_name = st.text_input(
                "브랜드명",
                value=SessionManager.get("brand_name", ""),
                placeholder="예: 자연담은",
                help="제품의 브랜드 또는 회사명을 입력하세요"
            )
        
        with col2:
            product_usage = st.text_input(
                "제품 용도/카테고리",
                value=SessionManager.get("product_usage", ""),
                placeholder="예: 건강한 간식, 요리 재료",
                help="제품이 사용되는 목적이나 카테고리를 입력하세요"
            )
            
            target_audience = st.selectbox(
                "타겟 고객층",
                ["전체", "10-20대", "20-30대", "30-40대", "40-50대", "50대 이상"],
                help="주요 타겟 고객층을 선택하세요"
            )
        
        st.markdown("#### ✨ 상세 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            key_features = st.text_area(
                "주요 특징/장점",
                value=SessionManager.get("key_features", ""),
                placeholder="예: 무농약 재배, 당도 높음, 비타민 C 풍부",
                height=80,
                help="제품의 주요 특징이나 장점을 나열하세요"
            )
        
        with col2:
            additional_info = st.text_area(
                "추가 정보",
                value=SessionManager.get("additional_info", ""),
                placeholder="예: 할인 행사, 이벤트 정보, 특별한 메시지",
                height=80,
                help="할인 정보, 이벤트, 특별한 메시지 등을 입력하세요"
            )
        
        # 톤앤매너 설정
        st.markdown("#### 🎭 광고 톤앤매너")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tone = st.selectbox(
                "광고 톤",
                ["친근한", "전문적인", "감성적인", "유머러스", "신뢰감 있는", "트렌디한"],
                help="원하는 광고의 느낌을 선택하세요"
            )
        
        with col2:
            style = st.selectbox(
                "문체",
                ["반말", "존댓말", "단문", "서술형", "질문형", "감탄형"],
                help="광고 문구의 문체를 선택하세요"
            )
        
        with col3:
            length = st.selectbox(
                "문구 길이",
                ["짧게 (10자 이내)", "보통 (20자 내외)", "길게 (30자 이상)"],
                help="원하는 광고 문구의 길이를 선택하세요"
            )
        
        # 생성 버튼
        submitted = st.form_submit_button("🤖 AI 광고 문구 생성", type="primary", use_container_width=True)
        
        if submitted:
            # 필수 정보 검증
            if not all([product_name.strip(), product_usage.strip(), brand_name.strip()]):
                st.error("⚠️ 제품명, 용도, 브랜드명은 필수 항목입니다.")
                return
            
            # 세션에 저장
            SessionManager.update({
                "product_name": product_name,
                "product_usage": product_usage,
                "brand_name": brand_name,
                "target_audience": target_audience,
                "key_features": key_features,
                "additional_info": additional_info,
                "tone": tone,
                "style": style,
                "length": length
            })
            
            # AI 텍스트 생성 실행
            generate_ad_text_with_ai(api_client)

def generate_ad_text_with_ai(api_client):
    """AI를 통한 광고 텍스트 생성"""
    
    # 세션에서 정보 가져오기
    product_name = SessionManager.get("product_name")
    product_usage = SessionManager.get("product_usage")
    brand_name = SessionManager.get("brand_name")
    target_audience = SessionManager.get("target_audience", "전체")
    key_features = SessionManager.get("key_features", "")
    additional_info = SessionManager.get("additional_info", "")
    tone = SessionManager.get("tone", "친근한")
    style = SessionManager.get("style", "반말")
    length = SessionManager.get("length", "보통 (20자 내외)")
    
    # 상세한 프롬프트 구성
    detailed_prompt = f"""
    제품 정보:
    - 제품명: {product_name}
    - 브랜드: {brand_name}
    - 용도: {product_usage}
    - 타겟: {target_audience}
    - 특징: {key_features}
    - 추가 정보: {additional_info}
    
    광고 요구사항:
    - 톤: {tone}
    - 문체: {style}
    - 길이: {length}
    """
    
    with st.spinner("🤖 AI가 제품 정보를 분석하고 광고 문구를 생성하고 있습니다..."):
        try:
            generated_text = api_client.generate_ad_text(
                product_name=product_name,
                product_usage=product_usage,
                brand_name=brand_name,
                additional_info=detailed_prompt
            )
            
            if generated_text:
                SessionManager.set("generated_text", generated_text)
                st.success("✅ 광고 문구가 생성되었습니다!")
                st.rerun()
            else:
                st.error("❌ 광고 문구 생성에 실패했습니다. 다시 시도해주세요.")
                
        except Exception as e:
            st.error(f"광고 문구 생성 중 오류가 발생했습니다: {str(e)}")
            st.info("💡 입력 정보를 확인하고 다시 시도해주세요.")