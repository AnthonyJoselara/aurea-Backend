from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel


class CycleRecordInternal(BaseModel):
    id_registro: UUID
    id_paciente: UUID
    fecha: date
    flujo: Optional[str] = "ninguno"
    moco: Optional[str] = None
    temperatura_basal: Optional[Decimal] = None
    estado_animo: List[str] = []
    sintomas_fisicos: List[str] = []
    hubo_relaciones: bool = False
    proteccion_utilizada: bool = False
    anomalia_detectada: bool = False
    descripcion_anomalia: Optional[str] = None
    notas: Optional[str] = None
    creado_en: datetime
