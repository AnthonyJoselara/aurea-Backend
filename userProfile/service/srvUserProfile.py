from uuid import UUID
from userProfile.database.dbIntUserProfile import DbIntUserProfile
from userProfile.entities.profileRequests import UpdateGeneralProfileRequestDTO
from userProfile.entities.profileResponses import GeneralProfileResponseDTO
from userProfile.exceptions.userProfileExceptions import ProfileNotFoundException
from authentication.entities.authModels import AuthenticatedUser


class SrvUserProfile:
    """
    Servicio de Dominio enfocado exclusivamente en la identidad y perfil general del usuario.
    """
    def __init__(self, db: DbIntUserProfile):
        self._db = db

    async def getMyProfile(self, currentUser: AuthenticatedUser) -> GeneralProfileResponseDTO:
        record = await self._db.getProfileByUserId(currentUser.user_id)
        if not record:
            # Auto-provisionamiento si se autentica por primera vez
            record = await self._db.upsertProfile(
                user_id=currentUser.user_id,
                email=currentUser.email,
                nombre_completo=currentUser.nombre or "Usuaria Áurea",
                rol=currentUser.role
            )
        return GeneralProfileResponseDTO.model_validate(record)

    async def updateMyProfile(
        self,
        currentUser: AuthenticatedUser,
        data: UpdateGeneralProfileRequestDTO
    ) -> GeneralProfileResponseDTO:
        # Aseguramos que existe el perfil antes de actualizar
        existing = await self._db.getProfileByUserId(currentUser.user_id)
        if not existing:
            await self._db.upsertProfile(
                user_id=currentUser.user_id,
                email=currentUser.email,
                nombre_completo=currentUser.nombre or "Usuaria Áurea",
                rol=currentUser.role
            )

        updated = await self._db.updateProfile(currentUser.user_id, data)
        return GeneralProfileResponseDTO.model_validate(updated)
