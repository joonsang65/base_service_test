"""스타일 정의"""

# 사이드바 스타일
SIDEBAR_STYLES = {
    "container": {"padding": "1rem"},
    "icon": {"color": "#4A8CF1", "font-size": "20px"},
    "nav-link": {
        "font-size": "16px",
        "text-align": "left",
        "--hover-color": "#e6f0ff",
        "border-radius": "8px",
        "margin": "2px 0",
    },
    "nav-link-selected": {
        "background-color": "#4A8CF1",
        "color": "white",
        "font-weight": "bold",
        "border-radius": "8px",
    },
    "menu-title": {"font-size": "20px", "font-weight": "bold", "color": "#333"},
}

# 카드 스타일
CARD_CSS = """
<style>
.ad-card {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 10px 0;
    transition: all 0.3s ease;
    background: white;
}
.ad-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
.ad-card img {
    max-width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 12px;
}
.ad-card h4 {
    color: #333;
    margin: 12px 0 8px 0;
}
.ad-card p {
    color: #666;
    font-size: 14px;
    line-height: 1.4;
}
.ad-card .cta {
    color: #4A8CF1;
    font-weight: bold;
    margin-top: 8px;
}
</style>
"""

# 워크플로우 스타일
WORKFLOW_CSS = """
<style>
.workflow-container {
    background: #f8f9fa;
    padding: 24px;
    border-radius: 12px;
    margin: 16px 0;
    border: 1px solid #e9ecef;
}
.step-header {
    background: linear-gradient(90deg, #4A8CF1, #6c63ff);
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
}
.process-box {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin: 12px 0;
}
.status-success {
    border-left: 4px solid #28a745;
    background: #f8fff9;
}
.status-processing {
    border-left: 4px solid #ffc107;
    background: #fffef8;
}
.status-pending {
    border-left: 4px solid #e9ecef;
    background: #f8f9fa;
}
.image-preview {
    border: 2px dashed #dee2e6;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    background: #f8f9fa;
}
.image-preview.has-image {
    border: 2px solid #4A8CF1;
    background: white;
}
</style>
"""

# 갤러리 스타일
GALLERY_CSS = """
<style>
.gallery-slider {
    white-space: nowrap;
    overflow: hidden;
    position: relative;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 0;
    margin: 20px 0;
    border-radius: 12px;
}
.slide-track {
    display: inline-block;
    animation: scroll-left 60s linear infinite;
}
.slide-track img {
    height: 180px;
    margin: 0 12px;
    display: inline-block;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}
.slide-track img:hover {
    transform: scale(1.05);
}
@keyframes scroll-left {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
@keyframes scroll-right {
    0% { transform: translateX(0); }
    100% { transform: translateX(50%); }
}
.slider-right .slide-track {
    animation: scroll-right 70s linear infinite;
}
</style>
"""