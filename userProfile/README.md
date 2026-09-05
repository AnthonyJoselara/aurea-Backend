# Módulo: userProfile

## Responsabilidad Principal
Gestiona la identidad pública de la usuaria en `nucleo.perfiles` y su contexto fisiológico y biológico en `nucleo.perfiles_paciente`.

## Qué hace:
- Consulta y actualización de datos generales (nombre completo, avatar).
- Consulta y actualización de la ficha fisiológica de la paciente:
  - `etapa_actual`: 'ciclo_menstrual' | 'embarazo' | 'menopausia' | 'indeterminado'.
  - Parámetros basales: `fecha_ultima_regla`, `duracion_ciclo_dias`, `duracion_periodo_dias`.
  - Parámetros gestacionales: `fecha_probable_parto`, `semanas_embarazo_base`.
  - Parámetros de menopausia: `anios_en_transicion`.
- Reglas de validación biológica (ej: duración de ciclo válida entre 21 y 45 días, duración de periodo entre 2 y 10 días).

## Qué NO hace:
- NO registra síntomas diarios ni biomarcadores de un día puntual (delegado a `menstrualCycle`).
- NO gestiona credenciales de inicio de sesión ni contraseñas (delegado a Supabase Auth).

## Invariantes:
- Cada usuario autenticado solo puede consultar o modificar su propio perfil (`auth.uid() = id_usuario`).
