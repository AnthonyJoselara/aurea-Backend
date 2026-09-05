from datetime import date
from fastapi import APIRouter, Depends, Query, status
from authentication.dependencies.authDependencies import getAuthenticatedUser
from authentication.entities.authModels import AuthenticatedUser
from menstrualCycle.dependencies.menstrualCycleDependencies import getCycleDayLogService
from menstrualCycle.service.srvCycleDayLog import SrvCycleDayLog
from menstrualCycle.entities.cycleDayRequests import CreateOrUpdateCycleDayRequestDTO
from menstrualCycle.entities.cycleDayResponses import CycleDayResponseDTO, CycleDayHistoryResponseDTO

router = APIRouter(prefix="/cycles/days", tags=["Cycle Day Log"])


@router.post(
    "",
    response_model=CycleDayResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registra o actualiza biomarcadores de un día del ciclo (flujo, temperatura, síntomas)"
)
async def logCycleDay(
    data: CreateOrUpdateCycleDayRequestDTO,
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvCycleDayLog = Depends(getCycleDayLogService)
) -> CycleDayResponseDTO:
    return await service.logDay(currentUser, data)


@router.get(
    "/by-date/{recordDate}",
    response_model=CycleDayResponseDTO,
    summary="Consulta el registro de biomarcadores de una fecha específica"
)
async def getCycleDayByDate(
    recordDate: date,
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvCycleDayLog = Depends(getCycleDayLogService)
) -> CycleDayResponseDTO:
    return await service.getDay(currentUser, recordDate)


@router.get(
    "/history",
    response_model=CycleDayHistoryResponseDTO,
    summary="Obtiene el historial cronológico de registros en un rango de fechas"
)
async def getCycleHistory(
    startDate: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    endDate: date = Query(..., description="Fecha final (YYYY-MM-DD)"),
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvCycleDayLog = Depends(getCycleDayLogService)
) -> CycleDayHistoryResponseDTO:
    return await service.getHistory(currentUser, startDate, endDate)


@router.delete(
    "/by-date/{recordDate}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina el registro de una fecha"
)
async def deleteCycleDay(
    recordDate: date,
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvCycleDayLog = Depends(getCycleDayLogService)
):
    await service.removeDay(currentUser, recordDate)
