from fastapi.testclient import TestClient
from main import app
from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario
from unittest.mock import patch
from datetime import datetime

client = TestClient(app)

mock_user = Usuario(id=1, nombre="Test User", email="test@nymera.com")


def override_get_current_user():
    return mock_user


def test_create_sueno_unauthorized():
    """Verifica que intentar crear un sueño sin estar logueado rechaza la petición con 401 o 403."""
    app.dependency_overrides.pop(get_current_user, None)

    payload = {
        "titulo": "Sueño sin token",
        "contenido": "Contenido de prueba...",
        "categoria_id": 1,
        "idioma_original": "es",
        "publico": True,
    }

    response = client.post("/suenos", json=payload)
    assert response.status_code in [401, 403]


def test_create_sueno_missing_fields():
    """Verifica que Pydantic intercepta campos obligatorios faltantes (ej: sin título) devolviendo 422."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "contenido": "Falta el título...",
        "categoria_id": 1,
        "idioma_original": "es",
        "publico": True,
    }

    response = client.post("/suenos", json=payload)
    assert response.status_code == 422


def test_translate_sueno_invalid_language_pattern():
    """Verifica que el pattern de la traducción (solo 'es' o 'en') rechaza otros idiomas con 422."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/suenos/1/traduccion?idioma=fr")
    assert response.status_code == 422


def test_get_liked_suenos_user_mismatch():
    """Verifica que un usuario no puede consultar los likes de otro usuario (comparando IDs con 403)."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/suenos/usuarios/99/likes")
    assert response.status_code == 403


def test_update_sueno_not_found():
    """Edge Case: Intentar actualizar un sueño que no existe (debe devolver 400 o 404 según gestione el service)."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "titulo": "Sueño actualizado",
        "contenido": "Contenido nuevo...",
        "categoria_id": 1,
        "publico": True,
    }

    response = client.put("/suenos/9999", json=payload)
    assert response.status_code in [400, 404]


def test_delete_sueno_not_found():
    """Edge Case: Intentar borrar un sueño que no existe (debe devolver 404)."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.delete("/suenos/9999")
    assert response.status_code == 404


def test_toggle_like_unauthorized():
    """Verifica que intentar dar like a un sueño sin token de sesión rechaza la petición con 401 o 403."""
    app.dependency_overrides.pop(get_current_user, None)

    response = client.post("/suenos/1/like")
    assert response.status_code in [401, 403]


def test_create_comentario_missing_field():
    """Verifica que enviar un comentario sin los campos obligatorios (ej: contenido vacío) devuelve 422."""
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {}

    response = client.post("suenos/1/comentarios", json=payload)
    assert response.status_code == 422


def test_get_comentarios_public_access():
    """Verifica que cualquier usuario (incluso anónimo) puede leer los comentarios de un sueño público."""
    app.dependency_overrides.pop(get_current_user, None)

    response = client.get("/suenos/1/comentarios")
    assert response.status_code in [200, 404]


@patch("app.routers.sueno_router.sueno_service.create_sueno")
def test_create_sueno_success(mock_create):
    """Verifica la creación exitosa de un sueño (200 OK)."""
    mock_create.return_value = {
        "id": 1,
        "titulo": "Sueño de prueba",
        "preview_contenido": "Contenido...",
        "publico": True,
        "fecha_creacion": datetime.now(),
        "usuario_id": 1,
        "usuario_nombre": "Test User",
        "avatar_url": None,
        "categoria_id": 1,
        "categoria_nombre": "General",
        "likes_count": 0,
        "comentarios_count": 0,
        "liked_by_user": False,
        "idioma_original": "es",
    }
    app.dependency_overrides[get_current_user] = override_get_current_user

    payload = {
        "titulo": "Sueño de prueba",
        "contenido": "Contenido válido...",
        "categoria_id": 1,
        "idioma_original": "es",
        "publico": True,
    }
    response = client.post("/suenos", json=payload)
    assert response.status_code == 200


@patch(
    "app.routers.sueno_router.sueno_service.create_sueno",
    side_effect=ValueError("title_empty"),
)
def test_create_sueno_value_error(mock_create):
    """Verifica que un ValueError en el servicio de creación devuelve 400."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {
        "titulo": "",
        "contenido": "Contenido válido...",
        "categoria_id": 1,
        "idioma_original": "es",
        "publico": True,
    }
    response = client.post("/suenos", json=payload)
    assert response.status_code == 400


@patch("app.routers.sueno_router.sueno_service.update_sueno")
def test_update_sueno_success(mock_update):
    """Verifica la actualización exitosa de un sueño (200 OK)."""
    mock_update.return_value = {
        "id": 1,
        "titulo": "Sueño actualizado",
        "contenido": "Contenido nuevo...",
        "publico": True,
        "fecha_creacion": datetime.now(),
        "usuario_id": 1,
        "categoria_id": 1,
        "idioma_original": "es",
    }
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {
        "titulo": "Sueño actualizado",
        "contenido": "Contenido nuevo...",
        "categoria_id": 1,
        "publico": True,
    }
    response = client.put("/suenos/1", json=payload)
    assert response.status_code == 200


@patch(
    "app.routers.sueno_router.sueno_service.update_sueno", side_effect=PermissionError
)
def test_update_sueno_permission_error(mock_update):
    """Verifica que editar un sueño ajeno lanza 403."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {
        "titulo": "Sueño actualizado",
        "contenido": "Contenido nuevo...",
        "categoria_id": 1,
        "publico": True,
    }
    response = client.put("/suenos/1", json=payload)
    assert response.status_code == 403


@patch("app.routers.sueno_router.sueno_service.delete_sueno")
def test_delete_sueno_success(mock_delete):
    """Verifica el borrado exitoso de un sueño (204 No Content)."""
    mock_delete.return_value = None
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.delete("/suenos/1")
    assert response.status_code == 204


@patch(
    "app.routers.sueno_router.sueno_service.delete_sueno", side_effect=PermissionError
)
def test_delete_sueno_permission_error(mock_delete):
    """Verifica que borrar un sueño ajeno lanza 403."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.delete("/suenos/1")
    assert response.status_code == 403


@patch("app.routers.sueno_router.sueno_service.translate_sueno")
def test_translate_sueno_success(mock_translate):
    """Verifica la traducción exitosa de un sueño (200 OK)."""
    mock_translate.return_value = {
        "idioma": "en",
        "titulo": "Translated title",
        "contenido": "Translated content",
        "preview_contenido": "Translated...",
    }
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.get("/suenos/1/traduccion?idioma=en")
    assert response.status_code == 200


@patch(
    "app.routers.sueno_router.sueno_service.translate_sueno",
    side_effect=PermissionError,
)
def test_translate_sueno_permission_error(mock_translate):
    """Verifica que traducir un sueño privado sin permisos lanza 403."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.get("/suenos/1/traduccion?idioma=en")
    assert response.status_code == 403


@patch("app.routers.sueno_router.sueno_service.get_liked_suenos")
def test_get_liked_suenos_success(mock_get_liked):
    """Verifica la consulta exitosa de sueños likeados por el propio usuario (200 OK)."""
    mock_get_liked.return_value = []
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.get("/suenos/usuarios/1/likes")
    assert response.status_code == 200


@patch("app.routers.sueno_router.like_service.toggle_like")
def test_toggle_like_success(mock_toggle):
    """Verifica que dar like a un sueño funciona correctamente (200 OK)."""
    mock_toggle.return_value = {"status": "liked", "likes_count": 1,}
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.post("/suenos/1/like")
    assert response.status_code == 200


@patch("app.routers.sueno_router.comentario_service.create_comentario")
def test_create_comentario_success(mock_create):
    """Verifica la creación exitosa de un comentario (200 OK)."""
    mock_create.return_value = {
        "id": 1,
        "contenido": "Comentario de prueba",
        "fecha_creacion": datetime.now(),
        "usuario_id": 1,
        "usuario_nombre": "Test User",
        "avatar_url": None,
        "sueno_id": 1,
        "idioma_original": "es",
    }
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {"contenido": "Comentario de prueba", "idioma_original": "es"}
    response = client.post("/suenos/1/comentarios", json=payload)
    assert response.status_code == 200


@patch(
    "app.routers.sueno_router.comentario_service.create_comentario",
    side_effect=ValueError("content_empty"),
)
def test_create_comentario_value_error(mock_create):
    """Verifica que un ValueError al crear comentario devuelve 400."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {"contenido": "", "idioma_original": "es"}
    response = client.post("/suenos/1/comentarios", json=payload)
    assert response.status_code == 400


@patch(
    "app.routers.sueno_router.comentario_service.create_comentario",
    side_effect=PermissionError,
)
def test_create_comentario_permission_error(mock_create):
    """Verifica que un PermissionError al crear comentario devuelve 403."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    payload = {"contenido": "Comentario válido", "idioma_original": "es"}
    response = client.post("/suenos/1/comentarios", json=payload)
    assert response.status_code == 403


@patch(
    "app.routers.sueno_router.sueno_service.translate_sueno",
    side_effect=ValueError("dream_not_found"),
)
def test_translate_sueno_not_found(mock_translate):
    """Verifica que traducir un sueño que no existe devuelve un 404 limpio."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    response = client.get("/suenos/9999/traduccion?idioma=en")
    assert response.status_code == 404


@patch("app.routers.sueno_router.sueno_service.get_sueno_detalles")
def test_get_sueno_detalles_anonymous(mock_get_detalles):
    """Verifica que un usuario anónimo puede ver el detalle de un sueño público (200 OK)."""
    mock_get_detalles.return_value = {
        "id": 1,
        "titulo": "Sueño detallado",
        "contenido": "Contenido completo del sueño...",
        "fecha_creacion": datetime.now(),
        "usuario_id": 1,
        "usuario_nombre": "Test User",
        "avatar_url": None,
        "likes_count": 0,
        "comentarios_count": 0,
        "liked_by_user": False,
        "publico": True,
        "categoria_id": 1,
        "categoria_nombre": "General",
        "idioma_original": "es"
    }
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/suenos/1")
    assert response.status_code == 200
    
app.dependency_overrides[get_current_user] = override_get_current_user