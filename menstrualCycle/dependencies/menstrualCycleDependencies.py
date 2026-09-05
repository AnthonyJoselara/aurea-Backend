from menstrualCycle.database.impDatabase.impPostgresCycleDayLog import ImpPostgresCycleDayLog
from menstrualCycle.database.impDatabase.impPostgresCyclePredictions import ImpPostgresCyclePredictions
from menstrualCycle.database.impDatabase.impPostgresDoctorCycleAccess import ImpPostgresDoctorCycleAccess
from menstrualCycle.service.srvCycleDayLog import SrvCycleDayLog
from menstrualCycle.service.srvCyclePredictions import SrvCyclePredictions
from menstrualCycle.service.srvDoctorCycleAccess import SrvDoctorCycleAccess

# Singletons de persistencia
_cycleDayLogDb = ImpPostgresCycleDayLog()
_cyclePredictionsDb = ImpPostgresCyclePredictions()
_doctorCycleAccessDb = ImpPostgresDoctorCycleAccess()


def getCycleDayLogService() -> SrvCycleDayLog:
    return SrvCycleDayLog(db=_cycleDayLogDb)


def getCyclePredictionsService() -> SrvCyclePredictions:
    return SrvCyclePredictions(db=_cyclePredictionsDb)


def getDoctorCycleAccessService() -> SrvDoctorCycleAccess:
    return SrvDoctorCycleAccess(db=_doctorCycleAccessDb)
