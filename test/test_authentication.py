from uuid import uuid4
from .conftest import create_token


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_protected_route_without_token(client):
    response = client.get("/api/profile/me")
    assert response.status_code == 401
    assert response.json()["error"]["module"] == "authentication"


def test_protected_route_with_expired_token(client):
    token = create_token(user_id=str(uuid4()), expired=True)
    response = client.get("/api/profile/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["error"]["module"] == "authentication"


def test_role_restriction_doctor_only(client, patient_user):
    # Un paciente intentando acceder a una ruta exclusiva de doctor
    random_patient_id = str(uuid4())
    response = client.get(
        f"/api/doctor/patient-cycles/{random_patient_id}/history?startDate=2026-01-01&endDate=2026-01-31",
        headers=patient_user["headers"]
    )
    assert response.status_code == 403
    assert response.json()["error"]["module"] == "authentication"
