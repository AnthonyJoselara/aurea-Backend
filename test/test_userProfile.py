def test_get_and_update_my_profile(client, patient_user):
    # 1. Obtener perfil (auto-provisionamiento en primer acceso)
    res_get = client.get("/api/profile/me", headers=patient_user["headers"])
    assert res_get.status_code == 200
    data_get = res_get.json()
    assert data_get["idUsuario"] == patient_user["user_id"]
    assert data_get["correo"] == "paciente@aurea.app"

    # 2. Actualizar nombre y avatar
    res_patch = client.patch(
        "/api/profile/me",
        headers=patient_user["headers"],
        json={
            "nombreCompleto": "Valentina Gómez",
            "avatarUrl": "https://aurea.app/avatars/val.png"
        }
    )
    assert res_patch.status_code == 200
    data_patch = res_patch.json()
    assert data_patch["nombreCompleto"] == "Valentina Gómez"
    assert data_patch["avatarUrl"] == "https://aurea.app/avatars/val.png"


def test_get_and_update_patient_context(client, patient_user):
    # 1. Obtener contexto biológico inicial (valores por defecto)
    res_get = client.get("/api/profile/patient-context", headers=patient_user["headers"])
    assert res_get.status_code == 200
    data = res_get.json()
    assert data["etapaActual"] == "indeterminado"
    assert data["duracionCicloDias"] == 28

    # 2. Actualizar parámetros biológicos
    res_patch = client.patch(
        "/api/profile/patient-context",
        headers=patient_user["headers"],
        json={
            "etapaActual": "ciclo_menstrual",
            "fechaUltimaRegla": "2026-08-20",
            "duracionCicloDias": 30,
            "duracionPeriodoDias": 5
        }
    )
    assert res_patch.status_code == 200
    updated = res_patch.json()
    assert updated["etapaActual"] == "ciclo_menstrual"
    assert updated["fechaUltimaRegla"] == "2026-08-20"
    assert updated["duracionCicloDias"] == 30


def test_invalid_life_stage_rejected(client, patient_user):
    res = client.patch(
        "/api/profile/patient-context",
        headers=patient_user["headers"],
        json={"etapaActual": "etapa_inexistente"}
    )
    assert res.status_code == 422
    assert res.json()["error"]["module"] == "userProfile"
