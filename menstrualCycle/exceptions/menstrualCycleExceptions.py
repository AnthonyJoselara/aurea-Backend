from uuid import UUID
from datetime import date
from globalDependencies.appBaseException import AppBaseException


class FutureDateNotAllowedException(AppBaseException):
    def __init__(self, provided_date: date):
        super().__init__(
            message=f"No es posible crear un registro de ciclo para una fecha futura ({provided_date}).",
            status_code=422,
            module="menstrualCycle",
            details={"providedDate": str(provided_date)}
        )


class CycleRecordNotFoundException(AppBaseException):
    def __init__(self, record_date: date):
        super().__init__(
            message=f"No se encontró ningún registro de ciclo para la fecha {record_date}.",
            status_code=404,
            module="menstrualCycle",
            details={"requestedDate": str(record_date)}
        )


class UnauthorizedClinicalAccessException(AppBaseException):
    def __init__(self, doctor_id: UUID, patient_id: UUID):
        super().__init__(
            message="Acceso denegado: El doctor no cuenta con una cita médica agendada o activa con la paciente solicitada.",
            status_code=403,
            module="menstrualCycle",
            details={"doctorId": str(doctor_id), "patientId": str(patient_id)}
        )
