from fastapi import APIRouter, Depends
from authentication.dependencies.authDependencies import getAuthenticatedUser
from authentication.entities.authModels import AuthenticatedUser
from userProfile.dependencies.userProfileDependencies import getPatientContextService
from userProfile.service.srvPatientContext import SrvPatientContext
from userProfile.entities.profileRequests import UpdatePatientContextRequestDTO
from userProfile.entities.profileResponses import PatientContextResponseDTO

router = APIRouter(prefix="/profile/patient-context", tags=["Patient Context"])


@router.get(
    "",
    response_model=PatientContextResponseDTO,
    summary="Obtiene la ficha fisiológica de la paciente (etapa de vida, FUR, duración del ciclo)"
)
async def getPatientContext(
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvPatientContext = Depends(getPatientContextService)
) -> PatientContextResponseDTO:
    return await service.getMyPatientContext(currentUser)


@router.patch(
    "",
    response_model=PatientContextResponseDTO,
    summary="Actualiza la etapa de vida o parámetros basales de la paciente"
)
async def updatePatientContext(
    data: UpdatePatientContextRequestDTO,
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvPatientContext = Depends(getPatientContextService)
) -> PatientContextResponseDTO:
    return await service.updateMyPatientContext(currentUser, data)
