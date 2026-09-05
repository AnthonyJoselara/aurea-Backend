from uuid import UUID
from globalDependencies.appBaseException import AppBaseException


class ProfileNotFoundException(AppBaseException):
    def __init__(self, user_id: UUID):
        super().__init__(
            message=f"No se encontró el perfil de usuario asociado al ID {user_id}.",
            status_code=404,
            module="userProfile",
            details={"userId": str(user_id)}
        )


class PatientContextNotFoundException(AppBaseException):
    def __init__(self, patient_id: UUID):
        super().__init__(
            message=f"No se encontró la ficha fisiológica para la paciente con ID {patient_id}.",
            status_code=404,
            module="userProfile",
            details={"patientId": str(patient_id)}
        )


class InvalidLifeStageException(AppBaseException):
    def __init__(self, stage: str):
        super().__init__(
            message=f"Etapa de vida '{stage}' inválida. Opciones válidas: 'ciclo_menstrual', 'embarazo', 'menopausia', 'indeterminado'.",
            status_code=422,
            module="userProfile",
            details={"providedStage": stage}
        )
