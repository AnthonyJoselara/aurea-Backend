from userProfile.database.dbIntPatientContext import DbIntPatientContext
from userProfile.entities.profileRequests import UpdatePatientContextRequestDTO
from userProfile.entities.profileResponses import PatientContextResponseDTO
from userProfile.exceptions.userProfileExceptions import InvalidLifeStageException
from authentication.entities.authModels import AuthenticatedUser

VALID_STAGES = {"ciclo_menstrual", "embarazo", "menopausia", "indeterminado"}


class SrvPatientContext:
    """
    Servicio de Dominio enfocado exclusivamente en la ficha contextual y fisiológica de la paciente.
    """
    def __init__(self, db: DbIntPatientContext):
        self._db = db

    async def getMyPatientContext(self, currentUser: AuthenticatedUser) -> PatientContextResponseDTO:
        record = await self._db.getPatientContext(currentUser.user_id)
        if not record:
            record = await self._db.createDefaultPatientContext(currentUser.user_id)
        return PatientContextResponseDTO.model_validate(record)

    async def updateMyPatientContext(
        self,
        currentUser: AuthenticatedUser,
        data: UpdatePatientContextRequestDTO
    ) -> PatientContextResponseDTO:
        if data.etapa_actual and data.etapa_actual not in VALID_STAGES:
            raise InvalidLifeStageException(data.etapa_actual)

        # Regla de coherencia fisiológica:
        # Si la duración del periodo supera la duración del ciclo, se ajusta o valida
        duracion_ciclo = data.duracion_ciclo_dias
        duracion_periodo = data.duracion_periodo_dias
        if duracion_ciclo and duracion_periodo and duracion_periodo >= duracion_ciclo:
            data.duracion_periodo_dias = min(duracion_periodo, duracion_ciclo - 10)

        record = await self._db.updatePatientContext(currentUser.user_id, data)
        return PatientContextResponseDTO.model_validate(record)
