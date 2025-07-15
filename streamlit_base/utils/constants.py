"""상수 정의"""

# 사용 가능한 폰트 목록
AVAILABLE_FONTS = {
    "Noto Sans KR": "Noto Sans Korean",
    "본고딕 Regular": "Source Han Sans KR Regular",
    "본고딕 Bold": "Source Han Sans KR Bold", 
    "나눔고딕": "NanumGothic",
    "나눔명조": "NanumMyeongjo",
    "배민 한나체": "BMHANNA",
    "쿠키런 Black": "CookieRun Black",
    "쿠키런 Bold": "CookieRun Bold",
    "쿠키런 Regular": "CookieRun Regular",
    "베이글팻원": "BagelFatOne Regular",
    "기후위기": "ClimateCrisis",
    "파셜산스": "PartialSansKR Regular"
}

# 플랫폼별 권장 설정
PLATFORM_RECOMMENDATIONS = {
    "인스타그램": {
        "canvas_size": (1080, 1080),
        "text_size_range": (60, 120),
        "recommended_fonts": ["쿠키런 Bold", "베이글팻원", "나눔고딕"],
        "color_schemes": ["활력", "모던", "트렌디"]
    },
    "블로그": {
        "canvas_size": (800, 600), 
        "text_size_range": (40, 80),
        "recommended_fonts": ["본고딕 Regular", "나눔명조", "Noto Sans KR"],
        "color_schemes": ["클래식", "모던", "자연"]
    },
    "포스터": {
        "canvas_size": (600, 800),
        "text_size_range": (80, 150),
        "recommended_fonts": ["본고딕 Bold", "쿠키런 Black", "기후위기"],
        "color_schemes": ["럭셔리", "활력", "선셋"]
    }
}

# 색상 팔레트
COLOR_PALETTES = {
    "브랜드 컬러": {
        "primary": "#4A8CF1",
        "secondary": "#6C63FF", 
        "accent": "#FF6B9D",
        "neutral": "#F8F9FA"
    },
    "자연": {
        "primary": "#27AE60",
        "secondary": "#2ECC71",
        "accent": "#F39C12",
        "neutral": "#ECF0F1"
    },
    "도시": {
        "primary": "#34495E",
        "secondary": "#2C3E50",
        "accent": "#E74C3C", 
        "neutral": "#BDC3C7"
    }
}

# 파일 형식 설정
SUPPORTED_IMAGE_FORMATS = {
    "input": ["png", "jpg", "jpeg", "webp"],
    "output": ["png", "jpg", "pdf"]
}

# UI 메시지
UI_MESSAGES = {
    "loading": {
        "background_removal": "🤖 AI가 배경을 제거하고 있습니다...",
        "background_generation": "🎨 AI가 배경을 생성하고 있습니다...",
        "text_generation": "✍️ AI가 광고 문구를 작성하고 있습니다...",
        "text_image_creation": "🎨 텍스트 이미지를 생성하고 있습니다...",
        "final_composition": "🎭 최종 이미지를 합성하고 있습니다..."
    },
    "success": {
        "step_1": "✅ 제품 이미지 설정이 완료되었습니다!",
        "step_2": "✅ 배경 이미지가 생성되었습니다!",
        "step_3": "✅ 광고 텍스트가 생성되었습니다!",
        "step_4": "🎉 광고가 완성되었습니다!"
    },
    "error": {
        "api_connection": "❌ 서버와의 연결에 문제가 있습니다.",
        "image_processing": "❌ 이미지 처리 중 오류가 발생했습니다.",
        "text_generation": "❌ 텍스트 생성에 실패했습니다.",
        "file_upload": "❌ 파일 업로드에 실패했습니다."
    }
}

# 성능 설정
PERFORMANCE_SETTINGS = {
    "max_image_size": (2048, 2048),
    "compression_quality": 85,
    "cache_ttl": 3600,  # 1시간
    "max_file_size_mb": 10
}