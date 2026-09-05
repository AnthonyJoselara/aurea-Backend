from datetime import date
from typing import Optional, List
from globalDependencies.sharedDTO import BaseSchema


class CyclePredictionResponseDTO(BaseSchema):
    dia_del_ciclo_actual: Optional[int] = None
    fase_actual: str  # 'menstruacion', 'folicular', 'ovulacion', 'lutea', 'desconocida'
    fecha_proxima_regla_estimada: Optional[date] = None
    fecha_ovulacion_estimada: Optional[date] = None
    inicio_ventana_fertil: Optional[date] = None
    fin_ventana_fertil: Optional[date] = None
    probabilidad_embarazo: str  # 'baja', 'media', 'alta'
    dias_restantes_para_periodo: Optional[int] = None
    consejo_clinico_del_dia: str
