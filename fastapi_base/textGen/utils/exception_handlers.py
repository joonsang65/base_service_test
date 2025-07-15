from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from fastapi_base.textGen.schemas.textGen_schemas import ErrorResponse

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: ValueError):
    """
    유효성 검사 예외 처리
    """
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=str(exc),
            error_code="VALIDATION_ERROR"
        ).dict()
    )

async def openai_exception_handler(request: Request, exc: Exception):
    """
    OpenAI API 예외 처리
    """
    logger.error(f"OpenAI error: {exc}")
    return JSONResponse(
        status_code=502,
        content=ErrorResponse(
            error="OpenAI 서비스 오류가 발생했습니다.",
            error_code="OPENAI_ERROR"
        ).dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    일반 예외 처리
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="서버 내부 오류가 발생했습니다.",
            error_code="INTERNAL_ERROR"
        ).dict()
    )