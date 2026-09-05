from uuid import UUID
from typing import Optional
from menstrualCycle.database.dbIntCyclePredictions import DbIntCyclePredictions
from userProfile.entities.profileInternal import PatientContextRecord
from globalDependencies.databaseConnection import dbState


class ImpPostgresCyclePredictions(DbIntCyclePredictions):
    """
    Implementación del acceso a los parámetros basales requeridos para el motor de predicción.
    """
    async def getPatientCycleBasals(self, patient_id: UUID) -> Optional[PatientContextRecord]:
        async with dbState.lock:
            row = dbState.perfiles_paciente.get(str(patient_id))
            if not row:
                return None
            return PatientContextRecord(**row)
