from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_lista_los_ejemplos_con_los_del_profesor_primero() -> None:
    respuesta = cliente.get("/api/v1/ejemplos")

    assert respuesta.status_code == 200
    ids = [ejemplo["id"] for ejemplo in respuesta.json()]
    assert ids == [
        "profesor-max",
        "profesor-min",
        "simplex-normal",
        "dos-fases-min",
        "infactible",
        "no-acotado",
        "optimos-multiples",
    ]


def test_ejemplo_del_profesor_tiene_los_datos_dictados() -> None:
    ejemplos = cliente.get("/api/v1/ejemplos").json()
    profesor = next(ejemplo for ejemplo in ejemplos if ejemplo["id"] == "profesor-max")

    assert profesor["problema"] == {
        "objetivo": "max",
        "coef_objetivo": ["10", "15"],
        "restricciones": [
            {"coeficientes": ["1", "0"], "signo": "<=", "lado_derecho": "400"},
            {"coeficientes": ["15", "20"], "signo": ">=", "lado_derecho": "500"},
            {"coeficientes": ["0", "8"], "signo": "=", "lado_derecho": "100"},
        ],
    }
