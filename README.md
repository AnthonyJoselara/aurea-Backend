# Aurea Health API — Documentacion Tecnica

## 1. Descripcion del Proyecto

Aurea es una solucion digital orientada a la salud femenina integral, el seguimiento biologico y el acompanamiento clinico supervisado. El backend proporciona una interfaz de programacion de aplicaciones bajo arquitectura REST, asincrona y modular, disenada para ofrecer alta disponibilidad, proteccion rigurosa de datos de salud y desacoplamiento de logica de negocio.

El sistema comprende las siguientes areas funcionales:

- Gestion de Identidad y Contexto Fisiologico: Administracion del perfil de usuarias y doctores, provisionamiento automatico en el primer inicio de sesion y seguimiento de la ficha fisiologica segun la etapa de vida (ciclo menstrual, gestacion, transicion climaterica o menopausia).
- Registro Diario de Biomarcadores: Captura idempotente de indicadores diarios tales como flujo sanguineo, caracteristicas del moco cervical, temperatura basal corporal, sintomas fisicos, estado animico, notas cualitativas y actividad sexual.
- Motor de Calculo y Predicciones Ginecologicas: Algoritmo determinista que procesa la fecha de ultima regla y las metricas basales para clasificar la fase hormonal activa (menstrual, folicular, ovulatoria o lutea), proyectar la ventana de fertilidad, estimar el dia de ovulacion y anticipar el siguiente periodo menstrual, emitiendo recomendaciones preventivas.
- Acceso Clinico Basado en Consentimiento: Mecanismo de autorizacion entre doctor y paciente que restringe la lectura de expedientes ginecologicos exclusivamente a medicos que cuenten con una cita activa o previa debidamente registrada.

## 2. Tecnologias Utilizadas

- FastAPI: Nucleo del backend asincrono en Python, seleccionado por su alto rendimiento en operaciones de entrada y salida, serializacion estricta y generacion nativa del estandar OpenAPI.
- Uvicorn: Servidor web ASGI de baja latencia encargado de despachar los procesos concurrentes de la aplicacion Python.
- Node.js y Express: Componente de pasarela de entrada (Gateway) y proxy inverso que orquesta la inicializacion del motor de FastAPI, supervisa el ciclo de vida del subproceso y gestiona el enrutamiento perimetral.
- TypeScript y TSX: Capa de ejecucion tipada para el Gateway, encargada de la gestion del proceso hijo y de devolver respuestas estructuradas ante eventuales indisponibilidades del servidor de aplicaciones.
- Pydantic: Biblioteca para definicion de esquemas de datos, validacion de tipos en tiempo de ejecucion y conversion transparente de nomenclatura entre el formato de transporte camelCase y el formato interno snake_case.
- PyJWT: Modulo criptografico para validacion de tokens web JSON con algoritmo HMAC-SHA256, verificacion de firmas y extraccion de roles y metadatos emitidos por el proveedor de autenticacion.
- Supabase y PostgreSQL: Motor relacional con diseno de base de datos segregado en esquemas independientes (nucleo, salud, clinica y comunidad). En entornos de pruebas unitarias y desarrollo local se utiliza una abstraccion concurrente en memoria protegida por bloqueos asincronos.
- Pytest y HTTPX: Marco de pruebas automatizadas para verificacion de integracion de rutas, seguridad de perfiles y aserciones de reglas de negocio.

## 3. Arquitectura y Comunicacion entre Componentes

La solucion implementa un patron de arquitectura limpia y modular por capas de responsabilidad:

- Capa Perimetral y Proxy Inverso: Las solicitudes externas arriban a la pasarela Node.js en el puerto asignado. La pasarela transmite el flujo HTTP directamente hacia el servidor ASGI FastAPI que opera internamente. Si el motor interno no se encuentra disponible, la pasarela intercepta el evento y retorna un error de servidor intermedio con estructura homologada.
- Capa de Seguridad y Filtros Transversales: La aplicacion intercepta cada peticion evaluando cabeceras de origen cruzado (CORS) y redirigiendo errores no capturados hacia manejadores globales. Mediante inyeccion de dependencias, se extrae el token Bearer, se valida su vigencia y se inyecta la entidad de usuario autenticado o se interrumpe la ejecucion con codigos de error de autorizacion.
- Capa de Enrutamiento y Validacion de Entrada: Los controladores reciben los datos de la solicitud, aplican validaciones semanticas de rango, longitud y tipo mediante esquemas de transferencia de datos (DTO), y delegan la ejecucion a la capa de servicio.
- Capa de Logica de Dominio y Servicios: Contiene las reglas operativas de la plataforma, el calculo de fases menstruales y la verificacion de permisos de relacion clinica. Los servicios operan de forma aislada y no dependen de detalles de infraestructura.
- Capa de Acceso a Datos e Interfaces: Los servicios interactuan unicamente con contratos e interfaces abstractas de persistencia, desacoplandose del controlador de base de datos subyacente.

En la dinamica clinica, la comunicacion entre modulos asegura que un usuario con perfil medico no pueda consultar el historial de ninguna paciente de forma directa: el servicio de acceso medico interroga primero al repositorio clinico para certificar la existencia de una cita valida entre ambos identificadores antes de consultar el registro de biomarcadores.

## 4. Instrucciones de Ejecucion

### Prerrequisitos
- Python 3.11 o superior y gestor de paquetes pip.
- Node.js 18 o superior y gestor de paquetes npm.

### Configuracion de Variables de Entorno
Copiar la plantilla de configuracion y ajustar los valores requeridos:

```bash
cp .env.example .env
```

### Modalidad 1: Ejecucion Integrada con Pasarela (Recomendada)
Esta modalidad inicia la pasarela Node.js en el puerto 3000 y levanta concurrentemente el servidor FastAPI en el puerto 8000:

```bash
npm install
pip install -r requirements.txt
npm run dev
```

### Modalidad 2: Ejecucion Directa con Python / Uvicorn
Para ejecutar unicamente el servidor ASGI de FastAPI en el puerto 3000 sin la pasarela de Node.js:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

En sistemas Windows, la activacion del entorno virtual se realiza con:

```bash
venv\Scripts\activate
```

### Verificacion de Estado y Documentacion
Una vez iniciado el servicio, los siguientes puntos de enlace permiten comprobar el estado del sistema y consultar los contratos interactivos de la API:

- Verificacion de salud: http://localhost:3000/health
- Documentacion interactiva Swagger UI: http://localhost:3000/docs
- Documentacion alternativa ReDoc: http://localhost:3000/redoc

### Ejecucion de Pruebas Automatizadas y Validacion de Tipos
Para ejecutar la suite completa de pruebas unitarias y de integracion:

```bash
pytest -v test/
```

O a traves del comando homologado en npm:

```bash
npm test
```

Para validar estaticamente los tipos del componente pasarela:

```bash
npm run lint
```

## 5. Puntos de Acceso del Sistema

- Estado y Monitoreo: Ruta publica para consultar el estado del servidor y verificar la salud de los servicios.
- Perfil General de Usuario: Rutas protegidas para consultar y actualizar la informacion basica de la cuenta activa (nombre, identificador y enlace de imagen).
- Ficha Fisiologica de la Paciente: Rutas para consultar y modificar la etapa reproductiva actual, la fecha de ultima regla, la duracion habitual del ciclo menstrual y la extension promedio del sangrado.
- Bitacora Diaria del Ciclo: Operaciones para registrar o actualizar los sintomas e indicadores de un dia determinado, consultar la informacion de una fecha especifica, solicitar el historial en un intervalo temporal o eliminar un registro puntual.
- Motor de Predicciones: Consulta automatizada que entrega la fase ginecologica del dia presente, proyeccion del siguiente periodo menstrual, estimacion de ventana fertil y consejos clinicos asociados.
- Consulta Medica Regulada: Ruta exclusiva para usuarios con rol de doctor que permite consultar el historial menstrual de una paciente, sujeta a la existencia de un vinculo clinico formal.

## 6. Reglas de Negocio, Seguridad e Invariantes

- Restriccion Temporal: La aplicacion deniega de forma estricta cualquier intento de asentar registros de biomarcadores o sintomas con fechas posteriores al dia calendario actual.
- Unicidad e Idempotencia: Cada paciente cuenta con un unico registro de seguimiento por dia. El envio reiterado de informacion para la misma fecha sobreescribe los campos correspondientes de forma idempotente en lugar de generar duplicados.
- Coherencia Fisiologica: La duracion estimada del sangrado menstrual no puede igualar ni sobrepasar la duracion total del ciclo de la paciente; el sistema ajusta o rechaza combinaciones que contradigan esta condicion biologica.
- Privacidad y Aislamiento de Expedientes: Los datos personales y clinicos estan vinculados al identificador unico del usuario autenticado. Ningun usuario puede alterar informacion de terceros y los profesionales medicos unicamente acceden a la informacion indispensable bajo consentimiento verificado.
- Manejo Homologado de Excepciones: Ninguna falla de infraestructura o error inesperado se remite en crudo al cliente. Todos los incidentes son procesados por la jerarquia de excepciones de la aplicacion, entregando respuestas uniformes que indican el modulo de origen, el mensaje tecnico, el codigo de estado HTTP y los detalles del suceso.
