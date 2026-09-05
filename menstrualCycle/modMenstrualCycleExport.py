from fastapi import APIRouter
from menstrualCycle.routers.rtrCycleDayLog import router as cycleDayLogRouter
from menstrualCycle.routers.rtrCyclePredictions import router as cyclePredictionsRouter
from menstrualCycle.routers.rtrDoctorCycleAccess import router as doctorCycleAccessRouter

modMenstrualCycleRouter = APIRouter()
modMenstrualCycleRouter.include_router(cycleDayLogRouter)
modMenstrualCycleRouter.include_router(cyclePredictionsRouter)
modMenstrualCycleRouter.include_router(doctorCycleAccessRouter)

__all__ = ["modMenstrualCycleRouter"]
