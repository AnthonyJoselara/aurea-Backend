from uuid import UUID
from datetime import date
from menstrualCycle.database.dbIntDoctorCycleAccess import DbIntDoctorCycleAccess
from menstrualCycle.entities.cycleDayResponses import CycleDayResponseDTO, CycleDayHistoryResponseDTO
from menstrualCycle.exceptions.menstrualCycleExceptions import UnauthorizedClinicalAccessException
from authentication.entities.authModels import AuthenticatedUser


class SrvDoctorCycleAccess:
    """
    Servicio de Dominio enfocado en la Dinámica Paciente ↔ Doctor.
    Verifica que el doctor autenticado cuente con consentimiento clínico (cita previa o agendada)
    antes de suministrar información médica de la paciente.
    """
    def __init__(self, db: DbIntDoctorCycleAccess):
        self._db = db

    async def getPatientHistoryForDoctor(
        self,
        currentDoctor: AuthenticatedUser,
        patient_id: UUID,
        start_date: date,
        end_date: date
    ) -> CycleDayHistoryResponseDTO:
        # Invariante de consentimiento: Verificar que el doctor tiene cita con esta paciente
        has_appointment = await self._db.hasActiveOrPastAppointment(
            doctor_id=currentDoctor.user_id,
            patient_id=patient_id
        )
        if not has_appointment:
            raise UnauthorizedClinicalAccessException(
                doctor_id=currentDoctor.user_id,
                patient_id=patient_id
            )

        records = await self._db.getPatientHistoryForDoctor(patient_id, start_date, end_date)
        dtos = [CycleDayResponseDTO.model_validate(r) for r in records]
        return CycleDayHistoryResponseDTO(
            total_registros=len(dtos),
            fecha_inicio=start_date,
            fecha_fin=end_date,
            registros=dtos
        )
