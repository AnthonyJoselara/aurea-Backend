import pytest
import jwt
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from main import app
from globalDependencies.config import settings
from globalDependencies.databaseConnection import dbState


@pytest.fixture(autouse=True)
def reset_database_state():
    """Limpia el estado de la base de datos en memoria antes de cada test."""
    dbState.clear()
    yield
    dbState.clear()


@pytest.fixture
def client():
    return TestClient(app)


def create_token(user_id: str, role: str = "paciente", email: str = "test@aurea.app", expired: bool = False) -> str:
    now = datetime.now(timezone.utc)
    exp = now - timedelta(hours=1) if expired else now + timedelta(hours=24)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "user_metadata": {
            "rol": role,
            "nombre_completo": f"Usuario {role}"
        },
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")


@pytest.fixture
def patient_user():
    user_id = str(uuid4())
    token = create_token(user_id=user_id, role="paciente", email="paciente@aurea.app")
    return {
        "user_id": user_id,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }


@pytest.fixture
def doctor_user():
    user_id = str(uuid4())
    token = create_token(user_id=user_id, role="doctor", email="doctor@aurea.app")
    return {
        "user_id": user_id,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }
