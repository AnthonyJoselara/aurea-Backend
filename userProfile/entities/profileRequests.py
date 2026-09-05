from typing import Optional
from datetime import date
from pydantic import Field
from globalDependencies.sharedDTO import BaseSchema


class UpdateGeneralProfileRequestDTO(BaseSchema):
    nombre_completo: Optional[str] = Field(None, min_length=2, max_length=150)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UpdatePatientContextRequestDTO(BaseSchema):
    etapa_actual: Optional[str] = Field(
        None,
        description="Etapa fisiológica: ciclo_menstrual, embarazo, menopausia o indeterminado"
    )
    fecha_ultima_regla: Optional[date] = None
    duracion_ciclo_dias: Optional[int] = Field(None, ge=18, le=60)
    duracion_periodo_dias: Optional[int] = Field(None, ge=1, le=15)
    fecha_probable_parto: Optional[date] = None
    semanas_embarazo_base: Optional[int] = Field(None, ge=1, le=45)
    anios_en_transicion: Optional[int] = Field(None, ge=0, le=30)
    notas_medicas_previas: Optional[str] = None
