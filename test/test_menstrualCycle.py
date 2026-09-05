from datetime import date, timedelta
from uuid import UUID
from globalDependencies.databaseConnection import dbState


def test_log_cycle_day_and_get_by_date(client, patient_user):
    today_str = date.today().isoformat()

    # 1. Registrar biomarcadores del día
    payload = {
        "fecha": today_str,
        "flujo": "moderado",
        "moco": "clara_de_huevo",
        "temperaturaBasal": 36.65,
        "estadoAnimo": ["tranquila", "concentrada"],
        "sintomasFisicos": ["colicos_leves"],
        "huboRelaciones": True,
        "proteccionUtilizada": True,
        "notas": "Día con energía estable"
    }
    res_post = client.post("/api/cycles/days", headers=patient_user["headers"], json=payload)
    assert res_post.status_code == 201
    data = res_post.json()
    assert data["fecha"] == today_str
    assert data["flujo"] == "moderado"
    assert data["moco"] == "clara_de_huevo"
    assert float(data["temperaturaBasal"]) == 36.65
    assert "tranquila" in data["estadoAnimo"]

    # 2. Consultar el registro creado por fecha
    res_get = client.get(f"/api/cycles/days/by-date/{today_str}", headers=patient_user["headers"])
    assert res_get.status_code == 200
    assert res_get.json()["idRegistro"] == data["idRegistro"]


def test_future_date_rejected(client, patient_user):
    future_date = (date.today() + timedelta(days=2)).isoformat()
    payload = {
        "fecha": future_date,
        "flujo": "ligero"
    }
    res = client.post("/api/cycles/days", headers=patient_user["headers"], json=payload)
    assert res.status_code == 422
    assert res.json()["error"]["module"] == "menstrualCycle"


def test_cycle_history_range(client, patient_user):
    # Insertamos 2 registros en días pasados
    d1 = (date.today() - timedelta(days=2)).isoformat()
    d2 = (date.today() - timedelta(days=1)).isoformat()

    client.post("/api/cycles/days", headers=patient_user["headers"], json={"fecha": d1, "flujo": "ligero"})
    client.post("/api/cycles/days", headers=patient_user["headers"], json={"fecha": d2, "flujo": "manchado"})

    # Consultamos el rango
    res = client.get(
        f"/api/cycles/days/history?startDate={d1}&endDate={d2}",
        headers=patient_user["headers"]
    )
    assert res.status_code == 200
    history = res.json()
    assert history["totalRegistros"] == 2
    assert len(history["registros"]) == 2


def test_cycle_predictions_engine(client, patient_user):
    # Configuramos la FUR 10 días atrás en el perfil de la paciente
    fur_date = (date.today() - timedelta(days=10)).isoformat()
    client.patch(
        "/api/profile/patient-context",
        headers=patient_user["headers"],
        json={
            "etapaActual": "ciclo_menstrual",
            "fechaUltimaRegla": fur_date,
            "duracionCicloDias": 28,
            "duracionPeriodoDias": 5
        }
    )

    # Calculamos predicciones
    res = client.get("/api/cycles/predictions/current", headers=patient_user["headers"])
    assert res.status_code == 200
    pred = res.json()
    assert pred["diaDelCicloActual"] == 11
    assert pred["faseActual"] in ["folicular", "ovulacion"]
    assert pred["fechaProximaReglaEstimada"] is not None


def test_doctor_access_without_appointment_is_forbidden(client, doctor_user, patient_user):
    patient_id = patient_user["user_id"]
    res = client.get(
        f"/api/doctor/patient-cycles/{patient_id}/history?startDate=2026-01-01&endDate=2026-01-31",
        headers=doctor_user["headers"]
    )
    assert res.status_code == 403
    assert res.json()["error"]["module"] == "menstrualCycle"


def test_doctor_access_with_registered_appointment_is_allowed(client, doctor_user, patient_user):
    patient_id = patient_user["user_id"]
    doctor_id = doctor_user["user_id"]
    today_str = date.today().isoformat()

    # La paciente crea un registro
    client.post("/api/cycles/days", headers=patient_user["headers"], json={"fecha": today_str, "flujo": "abundante"})

    # Simulamos la existencia de una cita médica entre el doctor y la paciente en clinica.citas
    dbState.citas["cita-1"] = {
        "id_doctor": UUID(doctor_id),
        "id_paciente": UUID(patient_id),
        "motivo": "Consulta de control ginecológico"
    }

    # El doctor ahora consulta con éxito
    res = client.get(
        f"/api/doctor/patient-cycles/{patient_id}/history?startDate={today_str}&endDate={today_str}",
        headers=doctor_user["headers"]
    )
    assert res.status_code == 200
    data = res.json()
    assert data["totalRegistros"] == 1
    assert data["registros"][0]["flujo"] == "abundante"
