from uuid import UUID
from typing import Optional, Tuple
from userProfile.database.dbIntUserProfile import DbIntUserProfile
from userProfile.database.dbIntPatientContext import DbIntPatientContext
from userProfile.entities.profileInternal import GeneralProfileRecord, PatientContextRecord


class DbUserProfileAdapter:
    """
    Adapter que coordina las operaciones entre 'nucleo.perfiles' y 'nucleo.perfiles_paciente'.
    """
    def __init__(self, profileDb: DbIntUserProfile, patientContextDb: DbIntPatientContext):
        self.profileDb = profileDb
        self.patientContextDb = patientContextDb

    async def getFullProfile(self, user_id: UUID) -> Tuple[Optional[GeneralProfileRecord], Optional[PatientContextRecord]]:
        profile = await self.profileDb.getProfileByUserId(user_id)
        patient_context = await self.patientContextDb.getPatientContext(user_id)
        return profile, patient_context
