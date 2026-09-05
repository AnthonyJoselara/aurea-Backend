from uuid import UUID
from datetime import date
from typing import List
from menstrualCycle.database.dbIntDoctorCycleAccess import DbIntDoctorCycleAccess
from menstrualCycle.entities.cycleInternalModels import CycleRecordInternal
from globalDependencies.databaseConnection import dbState


class ImpPostgresDoctorCycleAccess(DbIntDoctorCycleAccess):
    """
    Implementación del acceso clínico: valida contra 'clinica.citas' que el doctor
    posee una relación médica consentida antes de retornar los registros de 'salud.registros_ciclo'.
    """
    async def hasActiveOrPastAppointment(self, doctor_id: UUID, patient_id: UUID) -> bool:
        async with dbState.lock:
            for _, cita in dbState.citas.items():
                if cita.get("id_doctor") == doctor_id and cita.get("id_paciente") == patient_id:
                    return True
        return False

    async def getPatientHistoryForDoctor(
        self,
        patient_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[CycleRecordInternal]:
        results = []
        async with dbState.lock:
            for _, row in dbState.registros_ciclo.items():
                if row["id_paciente"] == patient_id and start_date <= row["fecha"] <= end_date:
                    results.append(CycleRecordInternal(**row))
        results.sort(key=lambda r: r.fecha, reverse=True)
        return results
