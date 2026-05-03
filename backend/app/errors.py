from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

logger = logging.getLogger(__name__)


class ApiError(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        detail: str,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = code


def bad_request(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_400_BAD_REQUEST, code=code, detail=detail)


def unauthorized(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_401_UNAUTHORIZED, code=code, detail=detail)


def forbidden(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_403_FORBIDDEN, code=code, detail=detail)


def conflict(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_409_CONFLICT, code=code, detail=detail)


def unprocessable_entity(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_422_UNPROCESSABLE_ENTITY, code=code, detail=detail)


def internal_server_error(code: str, detail: str) -> ApiError:
    return ApiError(status.HTTP_500_INTERNAL_SERVER_ERROR, code=code, detail=detail)


def _default_error_code(status_code: int) -> str:
    fallback_codes = {
        status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
        status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        status.HTTP_403_FORBIDDEN: "FORBIDDEN",
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
        status.HTTP_409_CONFLICT: "CONFLICT",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "UNPROCESSABLE_ENTITY",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "INTERNAL_SERVER_ERROR",
    }
    return fallback_codes.get(status_code, f"HTTP_{status_code}")


def _build_error_content(detail: Any, code: str, fallback_detail: str) -> dict[str, Any]:
    if isinstance(detail, dict):
        message = detail.get("detail") or detail.get("message") or fallback_detail
        content = {
            "detail": str(message),
            "code": str(detail.get("code") or code),
        }
        for key, value in detail.items():
            if key not in {"detail", "message", "code"}:
                content[key] = value
        return content

    if isinstance(detail, list):
        return {
            "detail": fallback_detail,
            "code": code,
            "errors": detail,
        }

    if detail is None:
        return {"detail": fallback_detail, "code": code}

    return {"detail": str(detail), "code": code}


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    fallback_detail = (
        "Validation error"
        if exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        else "Request failed"
    )
    code = getattr(exc, "code", None) or _default_error_code(exc.status_code)
    content = _build_error_content(exc.detail, code, fallback_detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=getattr(exc, "headers", None),
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "code": "REQUEST_VALIDATION_ERROR",
            "errors": exc.errors(),
        },
    )


async def unexpected_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "Unhandled exception during %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "code": "INTERNAL_SERVER_ERROR",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
