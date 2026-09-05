from uuid import UUID
from datetime import date
from menstrualCycle.database.dbIntCycleDayLog import DbIntCycleDayLog
from menstrualCycle.entities.cycleDayRequests import CreateOrUpdateCycleDayRequestDTO
from menstrualCycle.entities.cycleDayResponses import CycleDayResponseDTO, CycleDayHistoryResponseDTO
from menstrualCycle.exceptions.menstrualCycleExceptions import (
    FutureDateNotAllowedException,
    CycleRecordNotFoundException
)
from authentication.entities.authModels import AuthenticatedUser


class SrvCycleDayLog:
    """
    Servicio de Dominio encargado exclusivamente del registro diario de biomarcadores.
    """
    def __init__(self, db: DbIntCycleDayLog):
        self._db = db

    async def logDay(
        self,
        currentUser: AuthenticatedUser,
        data: CreateOrUpdateCycleDayRequestDTO
    ) -> CycleDayResponseDTO:
        # Invariante de negocio: No se permiten fechas futuras
        if data.fecha > date.today():
            raise FutureDateNotAllowedException(data.fecha)

        record = await self._db.upsertRecord(currentUser.user_id, data)
        return CycleDayResponseDTO.model_validate(record)

    async def getDay(
        self,
        currentUser: AuthenticatedUser,
        record_date: date
    ) -> CycleDayResponseDTO:
        record = await self._db.getRecordByDate(currentUser.user_id, record_date)
        if not record:
            raise CycleRecordNotFoundException(record_date)
        return CycleDayResponseDTO.model_validate(record)

    async def getHistory(
        self,
        currentUser: AuthenticatedUser,
        start_date: date,
        end_date: date
    ) -> CycleDayHistoryResponseDTO:
        records = await self._db.getHistoryInRange(currentUser.user_id, start_date, end_date)
        dtos = [CycleDayResponseDTO.model_validate(r) for r in records]
        return CycleDayHistoryResponseDTO(
            total_registros=len(dtos),
            fecha_inicio=start_date,
            fecha_fin=end_date,
            registros=dtos
        )

    async def removeDay(
        self,
        currentUser: AuthenticatedUser,
        record_date: date
    ) -> bool:
        existed = await self._db.deleteRecordByDate(currentUser.user_id, record_date)
        if not existed:
            raise CycleRecordNotFoundException(record_date)
        return True
