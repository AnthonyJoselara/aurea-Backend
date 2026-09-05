from uuid import UUID
from datetime import datetime, date
from typing import Optional
from globalDependencies.sharedDTO import BaseSchema


class GeneralProfileResponseDTO(BaseSchema):
    id_usuario: UUID
    nombre_completo: str
    correo: str
    rol: str
    avatar_url: Optional[str] = None
    fecha_registro: datetime
    actualizado_en: datetime


class PatientContextResponseDTO(BaseSchema):
    id_paciente: UUID
    etapa_actual: str
    fecha_ultima_regla: Optional[date] = None
    duracion_ciclo_dias: Optional[int] = 28
    duracion_periodo_dias: Optional[int] = 5
    fecha_probable_parto: Optional[date] = None
    semanas_embarazo_base: Optional[int] = None
    anios_en_transicion: Optional[int] = None
    notas_medicas_previas: Optional[str] = None


class FullUserProfileResponseDTO(BaseSchema):
    perfil: GeneralProfileResponseDTO
    contexto_paciente: Optional[PatientContextResponseDTO] = None
