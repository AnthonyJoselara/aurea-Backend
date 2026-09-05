from uuid import UUID, uuid4
from datetime import date, datetime, timezone
from typing import Optional, List
from menstrualCycle.database.dbIntCycleDayLog import DbIntCycleDayLog
from menstrualCycle.entities.cycleInternalModels import CycleRecordInternal
from menstrualCycle.entities.cycleDayRequests import CreateOrUpdateCycleDayRequestDTO
from globalDependencies.databaseConnection import dbState


class ImpPostgresCycleDayLog(DbIntCycleDayLog):
    """
    Implementación del acceso a la tabla 'salud.registros_ciclo'.
    Garantiza la clave única (id_paciente, fecha).
    """
    async def getRecordByDate(self, patient_id: UUID, record_date: date) -> Optional[CycleRecordInternal]:
        key = f"{patient_id}:{record_date}"
        async with dbState.lock:
            row = dbState.registros_ciclo.get(key)
            if not row:
                return None
            return CycleRecordInternal(**row)

    async def getHistoryInRange(
        self,
        patient_id: UUID,
        start_date: date,
        end_date: date
    ) -> List[CycleRecordInternal]:
        pid_str = str(patient_id)
        results = []
        async with dbState.lock:
            for key, row in dbState.registros_ciclo.items():
                if row["id_paciente"] == patient_id and start_date <= row["fecha"] <= end_date:
                    results.append(CycleRecordInternal(**row))
        # Orden cronológico descendente
        results.sort(key=lambda r: r.fecha, reverse=True)
        return results

    async def upsertRecord(
        self,
        patient_id: UUID,
        data: CreateOrUpdateCycleDayRequestDTO
    ) -> CycleRecordInternal:
        key = f"{patient_id}:{data.fecha}"
        now = datetime.now(timezone.utc)
        async with dbState.lock:
            existing = dbState.registros_ciclo.get(key)
            if existing:
                existing["flujo"] = data.flujo
                existing["moco"] = data.moco
                existing["temperatura_basal"] = data.temperatura_basal
                existing["estado_animo"] = data.estado_animo
                existing["sintomas_fisicos"] = data.sintomas_fisicos
                existing["hubo_relaciones"] = data.hubo_relaciones
                existing["proteccion_utilizada"] = data.proteccion_utilizada
                existing["anomalia_detectada"] = data.anomalia_detectada
                existing["descripcion_anomalia"] = data.descripcion_anomalia
                existing["notas"] = data.notas
                row = existing
            else:
                row = {
                    "id_registro": uuid4(),
                    "id_paciente": patient_id,
                    "fecha": data.fecha,
                    "flujo": data.flujo,
                    "moco": data.moco,
                    "temperatura_basal": data.temperatura_basal,
                    "estado_animo": data.estado_animo,
                    "sintomas_fisicos": data.sintomas_fisicos,
                    "hubo_relaciones": data.hubo_relaciones,
                    "proteccion_utilizada": data.proteccion_utilizada,
                    "anomalia_detectada": data.anomalia_detectada,
                    "descripcion_anomalia": data.descripcion_anomalia,
                    "notas": data.notas,
                    "creado_en": now
                }
                dbState.registros_ciclo[key] = row

            return CycleRecordInternal(**row)

    async def deleteRecordByDate(self, patient_id: UUID, record_date: date) -> bool:
        key = f"{patient_id}:{record_date}"
        async with dbState.lock:
            if key in dbState.registros_ciclo:
                del dbState.registros_ciclo[key]
                return True
            return False
