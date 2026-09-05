from globalDependencies.appBaseException import AppBaseException


class AuthenticationRequiredException(AppBaseException):
    def __init__(self, message: str = "Se requiere token de autenticación Bearer válido."):
        super().__init__(message=message, status_code=401, module="authentication")


class InvalidTokenException(AppBaseException):
    def __init__(self, message: str = "El token de autenticación es inválido o ha expirado."):
        super().__init__(message=message, status_code=401, module="authentication")


class InsufficientPermissionsException(AppBaseException):
    def __init__(self, required_role: str):
        super().__init__(
            message=f"No posee los permisos requeridos para esta acción (rol requerido: '{required_role}').",
            status_code=403,
            module="authentication",
            details={"requiredRole": required_role}
        )
