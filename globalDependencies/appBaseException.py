from typing import Optional, Any, Dict


class AppBaseException(Exception):
    """
    Excepción base para todos los errores de dominio en Áurea.
    Ninguna excepción cruda de infraestructura o base de datos debe escapar hacia el cliente.
    """
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        module: str = "core",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.module = module
        self.details = details or {}
