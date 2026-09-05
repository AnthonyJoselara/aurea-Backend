import jwt
from uuid import UUID
from typing import Optional, Callable
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authentication.entities.authModels import AuthenticatedUser
from authentication.exceptions.authExceptions import (
    AuthenticationRequiredException,
    InvalidTokenException,
    InsufficientPermissionsException
)
from globalDependencies.config import settings

http_bearer = HTTPBearer(auto_error=False)


async def getAuthenticatedUser(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> AuthenticatedUser:
    """
    Dependencia FastAPI que extrae el token Bearer, valida la identidad del usuario contra
    Supabase Auth (o firma JWT con el secreto de Supabase) y retorna el objeto AuthenticatedUser.
    """
    if not credentials or not credentials.credentials:
        raise AuthenticationRequiredException("Se requiere el encabezado 'Authorization: Bearer <token>'.")

    token = credentials.credentials

    try:
        # Decodificamos el token con el secreto de Supabase configurado
        # En modo debug/test si el secreto no coincide con un token mockeado, permitimos payload seguro de prueba
        try:
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("El token de autenticación ha expirado.")
        except Exception:
            # Fallback para pruebas o desarrollo con tokens decodificados sin verificación de firma estricta
            if settings.debug:
                payload = jwt.decode(token, options={"verify_signature": False, "verify_exp": True})
            else:
                raise

        user_id_str = payload.get("sub") or payload.get("user_id") or payload.get("id")
        if not user_id_str:
            raise InvalidTokenException("El token no contiene un identificador de usuario válido ('sub').")

        user_uuid = UUID(str(user_id_str))
        email = payload.get("email", "usuario@aurea.app")
        user_metadata = payload.get("user_metadata", {})
        role = payload.get("role") or user_metadata.get("rol") or user_metadata.get("role") or "paciente"
        nombre = user_metadata.get("nombre_completo") or payload.get("nombre")

        return AuthenticatedUser(
            user_id=user_uuid,
            email=email,
            role=role,
            nombre=nombre
        )
    except (ValueError, jwt.PyJWTError):
        raise InvalidTokenException("Token de autenticación corrupto, inválido o expirado.")


def requireRole(required_role: str) -> Callable:
    """
    Generador de dependencias para validar que el usuario tenga un rol específico (ej: 'doctor' o 'paciente').
    """
    async def roleChecker(
        current_user: AuthenticatedUser = Depends(getAuthenticatedUser)
    ) -> AuthenticatedUser:
        if current_user.role != required_role:
            raise InsufficientPermissionsException(required_role=required_role)
        return current_user

    return roleChecker
