from fastapi import Depends
from userProfile.database.impDatabase.impPostgresUserProfile import ImpPostgresUserProfile
from userProfile.database.impDatabase.impPostgresPatientContext import ImpPostgresPatientContext
from userProfile.service.srvUserProfile import SrvUserProfile
from userProfile.service.srvPatientContext import SrvPatientContext

# Singletons de persistencia para el ciclo de vida de la aplicación
_userProfileDb = ImpPostgresUserProfile()
_patientContextDb = ImpPostgresPatientContext()


def getUserProfileService() -> SrvUserProfile:
    return SrvUserProfile(db=_userProfileDb)


def getPatientContextService() -> SrvPatientContext:
    return SrvPatientContext(db=_patientContextDb)
