from uuid import UUID
from typing import Optional
from userProfile.database.dbIntPatientContext import DbIntPatientContext
from userProfile.entities.profileInternal import PatientContextRecord
from userProfile.entities.profileRequests import UpdatePatientContextRequestDTO
from userProfile.exceptions.userProfileExceptions import PatientContextNotFoundException
from globalDependencies.databaseConnection import dbState


class ImpPostgresPatientContext(DbIntPatientContext):
    """
    Implementación del acceso a la tabla 'nucleo.perfiles_paciente'.
    """
    async def getPatientContext(self, patient_id: UUID) -> Optional[PatientContextRecord]:
        async with dbState.lock:
            row = dbState.perfiles_paciente.get(str(patient_id))
            if not row:
                return None
            return PatientContextRecord(**row)

    async def createDefaultPatientContext(self, patient_id: UUID) -> PatientContextRecord:
        key = str(patient_id)
        async with dbState.lock:
            row = {
                "id_paciente": patient_id,
                "etapa_actual": "indeterminado",
                "fecha_ultima_regla": None,
                "duracion_ciclo_dias": 28,
                "duracion_periodo_dias": 5,
                "fecha_probable_parto": None,
                "semanas_embarazo_base": None,
                "anios_en_transicion": None,
                "notas_medicas_previas": None
            }
            dbState.perfiles_paciente[key] = row
            return PatientContextRecord(**row)

    async def updatePatientContext(
        self,
        patient_id: UUID,
        data: UpdatePatientContextRequestDTO
    ) -> PatientContextRecord:
        key = str(patient_id)
        async with dbState.lock:
            existing = dbState.perfiles_paciente.get(key)
            if not existing:
                # Si no existía por no haber pasado por el trigger, lo creamos
                existing = {
                    "id_paciente": patient_id,
                    "etapa_actual": "indeterminado",
                    "fecha_ultima_regla": None,
                    "duracion_ciclo_dias": 28,
                    "duracion_periodo_dias": 5,
                    "fecha_probable_parto": None,
                    "semanas_embarazo_base": None,
                    "anios_en_transicion": None,
                    "notas_medicas_previas": None
                }
                dbState.perfiles_paciente[key] = existing

            if data.etapa_actual is not None:
                existing["etapa_actual"] = data.etapa_actual
            if data.fecha_ultima_regla is not None:
                existing["fecha_ultima_regla"] = data.fecha_ultima_regla
            if data.duracion_ciclo_dias is not None:
                existing["duracion_ciclo_dias"] = data.duracion_ciclo_dias
            if data.duracion_periodo_dias is not None:
                existing["duracion_periodo_dias"] = data.duracion_periodo_dias
            if data.fecha_probable_parto is not None:
                existing["fecha_probable_parto"] = data.fecha_probable_parto
            if data.semanas_embarazo_base is not None:
                existing["semanas_embarazo_base"] = data.semanas_embarazo_base
            if data.anios_en_transicion is not None:
                existing["anios_en_transicion"] = data.anios_en_transicion
            if data.notas_medicas_previas is not None:
                existing["notas_medicas_previas"] = data.notas_medicas_previas

            return PatientContextRecord(**existing)
