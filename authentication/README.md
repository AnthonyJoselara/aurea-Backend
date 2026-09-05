# Módulo: authentication

## Responsabilidad Principal
Valida el token Bearer JWT emitido por Supabase Auth en las peticiones HTTP y construye el objeto de identidad autenticada (`AuthenticatedUser`) con su identificador único (`userId`), correo y rol (`paciente` o `doctor`).

## Qué hace:
- Extrae el token del header `Authorization: Bearer <token>`.
- Decodifica y valida la firma y expiración del JWT según la clave pública/secreto de Supabase.
- Provee la dependencia FastAPI `getAuthenticatedUser` para inyectar al usuario verificado en los routers.
- Provee la dependencia `requireRole('doctor' | 'paciente')` para restringir accesos clínicos.

## Qué NO hace:
- NO almacena contraseñas ni hashes (delegado a `auth.users` de Supabase).
- NO consulta datos fisiológicos ni clínicos de las usuarias (delegado a los módulos de dominio correspondientes).

## Invariantes y Reglas de Seguridad:
- Toda petición protegida debe responder HTTP 401 si el token no existe, está expirado o fue firmado con una clave distinta.
- En pruebas locales o mocks, se permite la decodificación de tokens de desarrollo garantizando siempre la estructura `sub: UUID`.
