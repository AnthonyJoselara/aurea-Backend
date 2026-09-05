from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from userProfile.entities.profileInternal import PatientContextRecord


class DbIntCyclePredictions(ABC):
    """
    Contrato abstracto para obtener los parámetros basales del ciclo (FUR, duración media)
    necesarios para el motor de predicción de fases.
    """
    @abstractmethod
    async def getPatientCycleBasals(self, patient_id: UUID) -> Optional[PatientContextRecord]:
        pass
