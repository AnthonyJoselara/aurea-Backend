from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import Field
from globalDependencies.sharedDTO import BaseSchema


class CreateOrUpdateCycleDayRequestDTO(BaseSchema):
    fecha: date = Field(..., description="Fecha del registro (no puede ser futura)")
    flujo: Optional[str] = Field(
        "ninguno",
        description="Opciones: ninguno, manchado, ligero, moderado, abundante"
    )
    moco: Optional[str] = Field(
        None,
        description="Opciones: seco, pegajoso, cremoso, clara_de_huevo, acuoso"
    )
    temperatura_basal: Optional[Decimal] = Field(
        None,
        ge=34.0,
        le=42.0,
        description="Temperatura basal corporal en grados Celsius (ej: 36.65)"
    )
    estado_animo: List[str] = Field(
        default_factory=list,
        description="Lista de estados emocionales (ej: ['tranquila', 'sensible', 'ansiosa'])"
    )
    sintomas_fisicos: List[str] = Field(
        default_factory=list,
        description="Lista de síntomas físicos (ej: ['colicos', 'dolor_lumbar', 'cefalea'])"
    )
    hubo_relaciones: bool = Field(False, description="Indica si hubo actividad sexual")
    proteccion_utilizada: bool = Field(False, description="Indica si se usó método de barrera/anticonceptivo")
    anomalia_detectada: bool = Field(False, description="Alerta de flujo atípico o dolor inusual")
    descripcion_anomalia: Optional[str] = None
    notas: Optional[str] = None
