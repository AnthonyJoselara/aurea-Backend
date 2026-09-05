from fastapi import APIRouter, Depends, status
from authentication.dependencies.authDependencies import getAuthenticatedUser
from authentication.entities.authModels import AuthenticatedUser
from userProfile.dependencies.userProfileDependencies import getUserProfileService
from userProfile.service.srvUserProfile import SrvUserProfile
from userProfile.entities.profileRequests import UpdateGeneralProfileRequestDTO
from userProfile.entities.profileResponses import GeneralProfileResponseDTO

router = APIRouter(prefix="/profile", tags=["User Profile"])


@router.get(
    "/me",
    response_model=GeneralProfileResponseDTO,
    summary="Obtiene el perfil general del usuario autenticado"
)
async def getMyProfile(
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvUserProfile = Depends(getUserProfileService)
) -> GeneralProfileResponseDTO:
    return await service.getMyProfile(currentUser)


@router.patch(
    "/me",
    response_model=GeneralProfileResponseDTO,
    summary="Actualiza campos del perfil general (nombre, avatar)"
)
async def updateMyProfile(
    data: UpdateGeneralProfileRequestDTO,
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvUserProfile = Depends(getUserProfileService)
) -> GeneralProfileResponseDTO:
    return await service.updateMyProfile(currentUser, data)
