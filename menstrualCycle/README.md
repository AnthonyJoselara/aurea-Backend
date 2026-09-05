# Módulo: menstrualCycle

## Responsabilidad Principal
Administra los registros diarios de la salud menstrual (`salud.registros_ciclo`), el cálculo de fases del ciclo (menstrual, folicular, ovulatoria, lútea) y el acceso clínico seguro y consentido para doctores.

## Qué hace:
- Registro y actualización diaria de biomarcadores (flujo, moco cervical, temperatura basal, estados de ánimo, síntomas físicos y notas).
- Consulta de registros por fecha específica y consulta de historiales en rangos de fechas.
- Algoritmo de estimación de fase y ventana fértil basado en la Fecha de Última Regla (FUR) y duración media del ciclo.
- Acceso médico: Permite a un doctor con cita agendada o completada (`clinica.citas`) consultar el historial de ciclos de su paciente.

## Qué NO hace:
- NO gestiona semanas de embarazo ni contracciones (delegado a `maternalHealth`).
- NO registra síntomas menopáusicos (delegado a `menopause`).
- NO agenda citas de telemedicina (delegado a `clinicalCare`).

## Invariantes y Reglas de Negocio:
- **Unicidad:** Solo se permite exactamente un registro por paciente y por fecha (`uq_paciente_fecha_ciclo`). Las actualizaciones son idempotentes vía upsert.
- **Fechas:** No se permite registrar días de ciclo en fechas futuras.
- **Acceso Médico:** Si un doctor intenta consultar el historial de una paciente sin tener una cita registrada con ella, se rechaza con error 403.
