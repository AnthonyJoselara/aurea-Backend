from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from userProfile.entities.profileInternal import GeneralProfileRecord
from userProfile.entities.profileRequests import UpdateGeneralProfileRequestDTO


class DbIntUserProfile(ABC):
    """
    Contrato abstracto para operaciones de persistencia en la tabla 'nucleo.perfiles'.
    """
    @abstractmethod
    async def getProfileByUserId(self, user_id: UUID) -> Optional[GeneralProfileRecord]:
        """Consulta el perfil público del usuario por su identificador UUID."""
        pass

    @abstractmethod
    async def upsertProfile(
        self,
        user_id: UUID,
        email: str,
        nombre_completo: str,
        rol: str = "paciente",
        avatar_url: Optional[str] = None
    ) -> GeneralProfileRecord:
        """Inserta o actualiza el perfil base del usuario."""
        pass

    @abstractmethod
    async def updateProfile(
        self,
        user_id: UUID,
        data: UpdateGeneralProfileRequestDTO
    ) -> GeneralProfileRecord:
        """Actualiza campos específicos del perfil."""
        pass
