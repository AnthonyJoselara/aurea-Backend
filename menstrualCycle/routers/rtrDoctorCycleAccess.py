from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query
from authentication.dependencies.authDependencies import requireRole
from authentication.entities.authModels import AuthenticatedUser
from menstrualCycle.dependencies.menstrualCycleDependencies import getDoctorCycleAccessService
from menstrualCycle.service.srvDoctorCycleAccess import SrvDoctorCycleAccess
from menstrualCycle.entities.cycleDayResponses import CycleDayHistoryResponseDTO

router = APIRouter(prefix="/doctor/patient-cycles", tags=["Doctor Clinical Access"])


@router.get(
    "/{patientId}/history",
    response_model=CycleDayHistoryResponseDTO,
    summary="Acceso médico al historial menstrual de una paciente (requiere rol doctor y cita registrada)"
)
async def getPatientHistoryForDoctor(
    patientId: UUID,
    startDate: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    endDate: date = Query(..., description="Fecha final (YYYY-MM-DD)"),
    currentDoctor: AuthenticatedUser = Depends(requireRole("doctor")),
    service: SrvDoctorCycleAccess = Depends(getDoctorCycleAccessService)
) -> CycleDayHistoryResponseDTO:
    return await service.getPatientHistoryForDoctor(currentDoctor, patientId, startDate, endDate)
