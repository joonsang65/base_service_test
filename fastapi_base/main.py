from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from textGen.routers import textGen, health
from imageGen_Text.routers import imageGen_Text_router
from imageGen_BG.routers import imageGen_BG_router

app = FastAPI(title="Multi-Service Backend", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(textGen.router, prefix="/api/v1/text", tags=["textGen"])
app.include_router(imageGen_Text_router.router, prefix="/api/v1/image/text", tags=["imgGen_Text"])
app.include_router(imageGen_BG_router.router, prefix="/api/v1/image/bg", tags=["imgGen_Backround"])

@app.get("/")
async def root():
    return {"message": "FastAPI Multi-Service Backend is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["textGen", "imageGen_Text_router"],
        "message": "All services are running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)