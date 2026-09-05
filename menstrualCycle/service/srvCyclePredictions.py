from datetime import date, timedelta
from typing import Optional
from menstrualCycle.database.dbIntCyclePredictions import DbIntCyclePredictions
from menstrualCycle.entities.predictionResponses import CyclePredictionResponseDTO
from authentication.entities.authModels import AuthenticatedUser


class SrvCyclePredictions:
    """
    Servicio de Dominio encargado exclusivamente del cálculo de fases y predicciones.
    Aplica las reglas ginecológicas estándar:
    - Fase menstrual: Días 1 a duracion_periodo
    - Ovulación estimada: 14 días antes del próximo ciclo esperado (Fase lútea típica de 14 días)
    - Ventana fértil: 5 días antes de la ovulación hasta 1 día después
    """
    def __init__(self, db: DbIntCyclePredictions):
        self._db = db

    async def calculatePredictions(self, currentUser: AuthenticatedUser) -> CyclePredictionResponseDTO:
        basals = await self._db.getPatientCycleBasals(currentUser.user_id)
        today = date.today()

        if not basals or not basals.fecha_ultima_regla:
            return CyclePredictionResponseDTO(
                dia_del_ciclo_actual=None,
                fase_actual="desconocida",
                fecha_proxima_regla_estimada=None,
                fecha_ovulacion_estimada=None,
                inicio_ventana_fertil=None,
                fin_ventana_fertil=None,
                probabilidad_embarazo="baja",
                dias_restantes_para_periodo=None,
                consejo_clinico_del_dia="Registra la fecha de tu última regla en tu perfil para habilitar predicciones personalizadas."
            )

        fur = basals.fecha_ultima_regla
        ciclo_dias = basals.duracion_ciclo_dias or 28
        periodo_dias = basals.duracion_periodo_dias or 5

        # Días transcurridos desde la FUR
        dias_transcurridos = (today - fur).days
        if dias_transcurridos < 0:
            dias_transcurridos = 0

        # Día del ciclo actual (1-indexed)
        dia_del_ciclo = (dias_transcurridos % ciclo_dias) + 1

        # Fechas proyectadas para el ciclo actual
        ciclo_actual_inicio = today - timedelta(days=dia_del_ciclo - 1)
        proxima_regla = ciclo_actual_inicio + timedelta(days=ciclo_dias)
        
        # Día de ovulación estimado = ciclo_dias - 14 días
        dia_ovulacion = max(periodo_dias + 1, ciclo_dias - 14)
        fecha_ovulacion = ciclo_actual_inicio + timedelta(days=dia_ovulacion - 1)
        inicio_ventana = fecha_ovulacion - timedelta(days=5)
        fin_ventana = fecha_ovulacion + timedelta(days=1)

        # Determinación de fase
        if dia_del_ciclo <= periodo_dias:
            fase = "menstruacion"
            probabilidad = "baja"
            consejo = "Descansa, mantente hidratada y cuida tu ingesta de hierro."
        elif dia_del_ciclo < dia_ovulacion - 2:
            fase = "folicular"
            probabilidad = "media"
            consejo = "Aumento de energía y estrógenos. Excelente momento para actividad física."
        elif dia_ovulacion - 2 <= dia_del_ciclo <= dia_ovulacion + 1:
            fase = "ovulacion"
            probabilidad = "alta"
            consejo = "Pico fértil. Puedes observar moco cervical tipo clara de huevo."
        else:
            fase = "lutea"
            probabilidad = "baja"
            consejo = "Fase progestacional. Prioriza el descanso y alimentos ricos en magnesio."

        dias_restantes = max(0, (proxima_regla - today).days)

        return CyclePredictionResponseDTO(
            dia_del_ciclo_actual=dia_del_ciclo,
            fase_actual=fase,
            fecha_proxima_regla_estimada=proxima_regla,
            fecha_ovulacion_estimada=fecha_ovulacion,
            inicio_ventana_fertil=inicio_ventana,
            fin_ventana_fertil=fin_ventana,
            probabilidad_embarazo=probabilidad,
            dias_restantes_para_periodo=dias_restantes,
            consejo_clinico_del_dia=consejo
        )
