import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from globalDependencies.appBaseException import AppBaseException

logger = logging.getLogger("aurea.globalHandler")


def registerGlobalExceptionHandlers(app: FastAPI) -> None:
    @app.exception_handler(AppBaseException)
    async def appBaseExceptionHandler(request: Request, exc: AppBaseException) -> JSONResponse:
        logger.warning(
            f"[{exc.module}] Error de dominio: {exc.message} (HTTP {exc.status_code}) en {request.url.path}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "module": exc.module,
                    "message": exc.message,
                    "statusCode": exc.status_code,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        formatted_errors = [
            {
                "field": ".".join(str(loc) for loc in err.get("loc", [])),
                "message": err.get("msg")
            }
            for err in errors
        ]
        logger.info(f"Error de validación en {request.url.path}: {formatted_errors}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "module": "validation",
                    "message": "Los datos enviados no cumplen con el formato requerido.",
                    "statusCode": 422,
                    "details": {"validationErrors": formatted_errors}
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandledExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Error no controlado en {request.url.path}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "module": "system",
                    "message": "Ocurrió un error interno en el servidor.",
                    "statusCode": 500,
                    "details": {}
                }
            }
        )
