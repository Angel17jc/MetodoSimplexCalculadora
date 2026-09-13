from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)

PROBLEMA = {
    "objetivo": "max",
    "coef_objetivo": ["3", "5"],
    "restricciones": [{"coeficientes": ["1", "0"], "signo": "<=", "lado_derecho": "4"}],
}


def test_contrato_tiene_todas_las_rutas_del_plan() -> None:
    rutas = app.openapi()["paths"]
    encontradas = {(ruta, metodo) for ruta, metodos in rutas.items() for metodo in metodos}

    assert encontradas >= {
        ("/api/v1/health", "get"),
        ("/api/v1/resolver", "post"),
        ("/api/v1/importar", "post"),
        ("/api/v1/exportar/pdf", "post"),
        ("/api/v1/problemas", "post"),
        ("/api/v1/problemas/{slug}", "get"),
        ("/api/v1/ejemplos", "get"),
    }


def test_resolver_documenta_la_respuesta_paso_a_paso() -> None:
    esquema = app.openapi()
    respuesta = esquema["paths"]["/api/v1/resolver"]["post"]["responses"]["200"]

    referencia = respuesta["content"]["application/json"]["schema"]["$ref"]
    assert referencia.endswith("/RespuestaResolver")
    assert "TipoPaso" in esquema["components"]["schemas"]


def test_endpoints_pendientes_responden_501() -> None:
    assert cliente.post("/api/v1/resolver", json=PROBLEMA).status_code == 501
    assert cliente.post("/api/v1/exportar/pdf", json=PROBLEMA).status_code == 501
    assert cliente.get("/api/v1/problemas/abc123").status_code == 501


def test_resolver_valida_el_problema_antes_de_responder() -> None:
    respuesta = cliente.post("/api/v1/resolver", json={"objetivo": "max"})

    assert respuesta.status_code == 422
