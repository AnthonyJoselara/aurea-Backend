from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from userProfile.database.dbIntUserProfile import DbIntUserProfile
from userProfile.entities.profileInternal import GeneralProfileRecord
from userProfile.entities.profileRequests import UpdateGeneralProfileRequestDTO
from userProfile.exceptions.userProfileExceptions import ProfileNotFoundException
from globalDependencies.databaseConnection import dbState


class ImpPostgresUserProfile(DbIntUserProfile):
    """
    Implementación del acceso a la tabla 'nucleo.perfiles'.
    Garantiza la correspondencia con los tipos de PostgreSQL (UUID, TIMESTAMPTZ, TEXT, rol_usuario).
    """
    async def getProfileByUserId(self, user_id: UUID) -> Optional[GeneralProfileRecord]:
        async with dbState.lock:
            row = dbState.perfiles.get(str(user_id))
            if not row:
                return None
            return GeneralProfileRecord(**row)

    async def upsertProfile(
        self,
        user_id: UUID,
        email: str,
        nombre_completo: str,
        rol: str = "paciente",
        avatar_url: Optional[str] = None
    ) -> GeneralProfileRecord:
        now = datetime.now(timezone.utc)
        user_key = str(user_id)
        async with dbState.lock:
            existing = dbState.perfiles.get(user_key)
            if existing:
                existing["nombre_completo"] = nombre_completo
                existing["correo"] = email
                existing["rol"] = rol
                if avatar_url is not None:
                    existing["avatar_url"] = avatar_url
                existing["actualizado_en"] = now
                row = existing
            else:
                row = {
                    "id_usuario": user_id,
                    "nombre_completo": nombre_completo,
                    "correo": email,
                    "rol": rol,
                    "avatar_url": avatar_url,
                    "fecha_registro": now,
                    "actualizado_en": now
                }
                dbState.perfiles[user_key] = row
            return GeneralProfileRecord(**row)

    async def updateProfile(
        self,
        user_id: UUID,
        data: UpdateGeneralProfileRequestDTO
    ) -> GeneralProfileRecord:
        now = datetime.now(timezone.utc)
        user_key = str(user_id)
        async with dbState.lock:
            existing = dbState.perfiles.get(user_key)
            if not existing:
                raise ProfileNotFoundException(user_id)

            if data.nombre_completo is not None:
                existing["nombre_completo"] = data.nombre_completo
            if data.avatar_url is not None:
                existing["avatar_url"] = data.avatar_url
            existing["actualizado_en"] = now

            return GeneralProfileRecord(**existing)
