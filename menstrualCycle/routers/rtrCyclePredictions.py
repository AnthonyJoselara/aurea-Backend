from fastapi import APIRouter, Depends
from authentication.dependencies.authDependencies import getAuthenticatedUser
from authentication.entities.authModels import AuthenticatedUser
from menstrualCycle.dependencies.menstrualCycleDependencies import getCyclePredictionsService
from menstrualCycle.service.srvCyclePredictions import SrvCyclePredictions
from menstrualCycle.entities.predictionResponses import CyclePredictionResponseDTO

router = APIRouter(prefix="/cycles/predictions", tags=["Cycle Predictions"])


@router.get(
    "/current",
    response_model=CyclePredictionResponseDTO,
    summary="Calcula la fase actual, ventana fértil y próxima regla proyectada"
)
async def getCurrentPredictions(
    currentUser: AuthenticatedUser = Depends(getAuthenticatedUser),
    service: SrvCyclePredictions = Depends(getCyclePredictionsService)
) -> CyclePredictionResponseDTO:
    return await service.calculatePredictions(currentUser)
