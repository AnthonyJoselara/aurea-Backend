from abc import ABC, abstractmethod
from uuid import UUID
from datetime import date
from typing import List
from menstrualCycle.entities.cycleInternalModels import CycleRecordInternal


class DbIntDoctorCycleAccess(ABC):
    """
    Contrato abstracto para la dinámica clínica Paciente ↔ Doctor.
    Verifica que exista una cita médica registrada en 'clinica.citas' antes de liberar datos íntimos.
    """
    @abstractmethod
    async def hasActiveOrPastAppointment(self, doctor_id: UUID, patient_id: UUID) -> bool:
        """Determina si el doctor tiene o tuvo una cita con la paciente solicitada."""
        pass

    @abstractmethod
    async def getPatientHistoryForDoctor(
        self,
        patient_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[CycleRecordInternal]:
        """Obtiene el historial de ciclos para la revisión del profesional."""
        pass
