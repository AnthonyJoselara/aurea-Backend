from fastapi import APIRouter
from userProfile.routers.rtrUserProfile import router as userProfileRouter
from userProfile.routers.rtrPatientContext import router as patientContextRouter

modUserProfileRouter = APIRouter()
modUserProfileRouter.include_router(userProfileRouter)
modUserProfileRouter.include_router(patientContextRouter)

__all__ = ["modUserProfileRouter"]
