from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from globalDependencies.config import settings
from globalDependencies.globalHandler import registerGlobalExceptionHandlers
from userProfile.modUserProfileExport import modUserProfileRouter
from menstrualCycle.modMenstrualCycleExport import modMenstrualCycleRouter

app = FastAPI(
    title="Áurea Health API",
    description="Backend modular REST para Áurea: salud menstrual, acompañamiento clínico y comunidad.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers Globales
registerGlobalExceptionHandlers(app)

# Registro de Módulos de Dominio
app.include_router(modUserProfileRouter, prefix="/api")
app.include_router(modMenstrualCycleRouter, prefix="/api")


@app.get("/health", tags=["System"])
async def healthCheck():
    return {
        "status": "healthy",
        "service": "aurea-backend",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
