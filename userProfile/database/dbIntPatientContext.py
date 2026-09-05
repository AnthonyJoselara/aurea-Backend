from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from userProfile.entities.profileInternal import PatientContextRecord
from userProfile.entities.profileRequests import UpdatePatientContextRequestDTO


class DbIntPatientContext(ABC):
    """
    Contrato abstracto para operaciones de persistencia en la tabla 'nucleo.perfiles_paciente'.
    """
    @abstractmethod
    async def getPatientContext(self, patient_id: UUID) -> Optional[PatientContextRecord]:
        """Consulta la ficha contextual y fisiológica de la paciente."""
        pass

    @abstractmethod
    async def createDefaultPatientContext(self, patient_id: UUID) -> PatientContextRecord:
        """Crea el contexto base inicializado con valores por defecto para una nueva paciente."""
        pass

    @abstractmethod
    async def updatePatientContext(
        self,
        patient_id: UUID,
        data: UpdatePatientContextRequestDTO
    ) -> PatientContextRecord:
        """Actualiza la etapa de vida o los parámetros basales de la paciente."""
        pass
