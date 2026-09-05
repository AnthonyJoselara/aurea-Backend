from abc import ABC, abstractmethod
from uuid import UUID
from datetime import date
from typing import Optional, List
from menstrualCycle.entities.cycleInternalModels import CycleRecordInternal
from menstrualCycle.entities.cycleDayRequests import CreateOrUpdateCycleDayRequestDTO


class DbIntCycleDayLog(ABC):
    """
    Contrato abstracto para operaciones de registro diario en 'salud.registros_ciclo'.
    """
    @abstractmethod
    async def getRecordByDate(self, patient_id: UUID, record_date: date) -> Optional[CycleRecordInternal]:
        """Consulta el registro biométrico de una fecha dada."""
        pass

    @abstractmethod
    async def getHistoryInRange(
        self,
        patient_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[CycleRecordInternal]:
        """Obtiene la lista de registros entre dos fechas inclusivas."""
        pass

    @abstractmethod
    async def upsertRecord(
        self,
        patient_id: UUID,
        data: CreateOrUpdateCycleDayRequestDTO
    ) -> CycleRecordInternal:
        """Inserta o actualiza atómicamente el registro del día (garantizando uq_paciente_fecha_ciclo)."""
        pass

    @abstractmethod
    async def deleteRecordByDate(self, patient_id: UUID, record_date: date) -> bool:
        """Elimina el registro de una fecha específica."""
        pass
