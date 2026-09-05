from typing import Dict, Any, List
import asyncio


class DatabaseState:
    """
    Representa el estado en memoria de los datos para tests y modo desarrollo/demostración,
    siguiendo estrictamente las tablas, tipos y relaciones de los esquemas PostgreSQL creados:
    - nucleo.perfiles
    - nucleo.perfiles_paciente
    - salud.registros_ciclo
    - salud.seguimiento_embarazo
    - clinica.perfiles_doctor
    - clinica.citas
    - comunidad.historias
    """
    def __init__(self):
        self.lock = asyncio.Lock()
        self.perfiles: Dict[str, Dict[str, Any]] = {}
        self.perfiles_paciente: Dict[str, Dict[str, Any]] = {}
        self.registros_ciclo: Dict[str, Dict[str, Any]] = {}  # key: f"{id_paciente}:{fecha}"
        self.perfiles_doctor: Dict[str, Dict[str, Any]] = {}
        self.citas: Dict[str, Dict[str, Any]] = {}

    def clear(self):
        self.perfiles.clear()
        self.perfiles_paciente.clear()
        self.registros_ciclo.clear()
        self.perfiles_doctor.clear()
        self.citas.clear()


dbState = DatabaseState()
