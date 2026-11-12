import pytest
from unittest.mock import MagicMock
from app.services.sueno_service import SuenoService


def test_create_sueno_title_too_short_raises_value_error():
    """Verifica que si el título es demasiado corto, el servicio lanza ValueError('title_too_short')."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    mock_translation_service = MagicMock()

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=mock_translation_service,
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Ab",
            contenido="Este es un contenido de prueba válido para el sueño.",
            usuario_id=1,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "title_too_short"

    mock_sueno_repo.create.assert_not_called()


def test_update_sueno_unauthorized_raises_permission_error():
    """Verifica que intentar editar un sueño que pertenece a otro usuario lanza PermissionError('unauthorized')."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(usuario_id=99, id=1)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=mock_translation_service,
    )

    with pytest.raises(PermissionError) as exc_info:
        service.update_sueno(
            sueno_id=1,
            titulo="Nuevo título válido",
            contenido="Nuevo contenido de prueba válido...",
            categoria_id=1,
            publico=True,
            usuario_actual_id=1,
        )

    assert str(exc_info.value) == "unauthorized"
    mock_sueno_repo.update.assert_not_called()


def test_translate_sueno_invalid_language_raises_value_error():
    """Verifica que solicitar una traducción a un idioma no soportado lanza ValueError('invalid_language')."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, publico=True, idioma_original="es"
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=mock_translation_service,
    )

    with pytest.raises(ValueError) as exc_info:
        service.translate_sueno(sueno_id=1, idioma_destino="de", usuario_actual_id=1)

    assert str(exc_info.value) == "invalid_language"


def test_extract_hashtags_normalizes_and_deduplicates():
    """Verifica que la función de hashtags extrae, limpia, pone en minúsculas y elimina duplicados."""
    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    texto = "Soñé con volar sobre #Madrid y #MADRID otra vez, viendo un #gran_cometa y #123."

    hashtags = service.extract_hashtags(texto)

    assert sorted(hashtags) == sorted(["madrid", "gran_cometa", "123"])


def test_translate_sueno_same_language_raises_value_error():
    """Caso raro: Intentar traducir un sueño al mismo idioma original debe lanzar ValueError('same_language')."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, publico=True, idioma_original="en"
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=mock_translation_service,
    )

    with pytest.raises(ValueError) as exc_info:
        service.translate_sueno(sueno_id=1, idioma_destino="en", usuario_actual_id=1)

    assert str(exc_info.value) == "same_language"
    mock_translation_service.translate.assert_not_called()


def test_get_feed_invalid_page_raises_value_error():
    """Solicitar una página menor a 1 en el feed debe lanzar ValueError('page_invalid')."""
    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.get_feed(page=0)

    assert str(exc_info.value) == "page_invalid"


def test_translate_sueno_uses_cached_translation():
    """Si la traducción ya existe en BD, la devuelve directamente y NO llama al servicio externo."""
    mock_sueno_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, publico=True, idioma_original="es"
    )

    mock_sueno_repo.get_traduccion.return_value = (
        "en",
        "Dream in English",
        "Content in English",
    )
    mock_sueno_repo.crear_preview.return_value = "Content in English..."

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=mock_translation_service,
    )

    resultado = service.translate_sueno(
        sueno_id=1, idioma_destino="en", usuario_actual_id=1
    )

    assert resultado["titulo"] == "Dream in English"
    assert resultado["idioma"] == "en"

    mock_translation_service.translate.assert_not_called()


def test_create_sueno_reuses_existing_hashtags():
    """Si un hashtag ya existe en la BD, se reutiliza en lugar de intentar insertarlo de nuevo."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()

    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = {"id": 1}

    mock_sueno = MagicMock(id=10)
    mock_sueno_repo.create.return_value = mock_sueno

    mock_hashtag_repo.get_by_nombre.return_value = MagicMock(id=5, nombre="magia")

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.create_sueno(
        titulo="Un sueño con #magia",
        contenido="Mucha magia por aquí.",
        usuario_id=1,
        categoria_id=1,
        idioma_original="es",
        publico=True,
    )

    mock_hashtag_repo.get_by_nombre.assert_called_once_with("magia")
    mock_hashtag_repo.insert.assert_not_called()

    mock_hashtag_repo.insert_sueno_hashtag.assert_called_once_with(10, 5)


def test_create_sueno_with_malicious_payload_handled_safely():
    """Caso de seguridad: Verifica que payloads con inyección XSS o SQL se procesan de forma segura como texto plano."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()

    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = {"id": 1}

    titulo_malicioso = "Sueño normal <script>alert('XSS')</script>"
    contenido_malicioso = (
        "Caminaba por la calle y de repente '; DROP TABLE usuarios; -- #peligro"
    )

    mock_sueno = MagicMock(id=15)
    mock_sueno_repo.create.return_value = mock_sueno

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.create_sueno(
        titulo=titulo_malicioso,
        contenido=contenido_malicioso,
        usuario_id=1,
        categoria_id=1,
        idioma_original="es",
        publico=True,
    )

    # Verifica que el repositorio recibe el texto literal
    mock_sueno_repo.create.assert_called_once_with(
        titulo_malicioso, contenido_malicioso, 1, 1, "es", True
    )

    # Comprobación extracción hashtag '#peligro'
    mock_hashtag_repo.get_by_nombre.assert_any_call("peligro")


def test_get_feed_passes_filters_to_repository():
    """Verifica que los filtros de categorías, orden y dirección se envían correctamente al repositorio."""
    mock_sueno_repo = MagicMock()
    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    service.get_feed(
        usuario_id=1, page=2, categorias=[3], ordenar_por="fecha", direccion="desc"
    )

    mock_sueno_repo.get_feed_detalle.assert_called_once_with(
        1, 20, 20, [3], "fecha", "desc"
    )


def test_create_sueno_content_too_short_raises_value_error():
    """Verifica que un contenido menor a 5 caracteres lanza ValueError('content_too_short')."""
    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Título válido",
            contenido="abc",
            usuario_id=1,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "content_too_short"


def test_create_sueno_category_not_found_raises_value_error():
    """Verifica que si la categoría no existe, lanza ValueError('category_not_found')."""
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()

    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = None  # Categoría no encontrada

    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Título válido",
            contenido="Contenido de prueba válido para el sueño.",
            usuario_id=1,
            categoria_id=999,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "category_not_found"


def test_create_sueno_user_not_found_raises_value_error():
    """Verifica que si el usuario no existe, lanza ValueError('user_does_not_exist')."""
    mock_usuario_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = None  # Usuario no existe

    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Título válido",
            contenido="Contenido de prueba válido para el sueño.",
            usuario_id=999,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "user_does_not_exist"


def test_create_sueno_success_flow():
    """Verifica el flujo completo y exitoso de creación de un sueño con inserción de hashtags nuevos."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()

    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = {"id": 1}

    mock_sueno_creado = MagicMock(id=42)
    mock_sueno_repo.create.return_value = mock_sueno_creado

    mock_hashtag_repo.get_by_nombre.return_value = None
    mock_hashtag_nuevo = MagicMock(id=7)
    mock_hashtag_repo.insert.return_value = mock_hashtag_nuevo

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.create_sueno(
        titulo="Sueño con #aventura",
        contenido="Fue una gran aventura espacial.",
        usuario_id=1,
        categoria_id=1,
        idioma_original="es",
        publico=True,
    )

    mock_hashtag_repo.insert.assert_called_once_with("aventura")
    mock_hashtag_repo.insert_sueno_hashtag.assert_called_once_with(42, 7)
    mock_sueno_repo.get_feed_item_by_id.assert_called_once_with(42, 1)


def test_update_sueno_success_flow():
    """Verifica el flujo completo y exitoso de actualización de un sueño por su autor."""
    mock_sueno_repo = MagicMock()
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_existente = MagicMock(usuario_id=1, id=1)
    mock_sueno_repo.get_by_id.return_value = mock_sueno_existente

    mock_categoria_repo.get_by_id.return_value = {"id": 2}

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=mock_hashtag_repo,
        translation_service=mock_translation_service,
    )

    service.update_sueno(
        sueno_id=1,
        titulo="Título actualizado correctamente",
        contenido="Este es el nuevo contenido válido del sueño con #novedad.",
        categoria_id=2,
        publico=False,
        usuario_actual_id=1,  # Coincide con el dueño (usuario_id=1)
    )

    mock_sueno_repo.update.assert_called_once()


def test_delete_sueno_success():
    """Verifica que el autor puede eliminar su propio sueño correctamente."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    service.delete_sueno(sueno_id=1, usuario_actual_id=1)

    mock_sueno_repo.delete.assert_called_once_with(1)


def test_delete_sueno_unauthorized_raises_permission_error():
    """Verifica que intentar eliminar un sueño de otro usuario lanza PermissionError('unauthorized')."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=99)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(PermissionError) as exc_info:
        service.delete_sueno(sueno_id=1, usuario_actual_id=1)

    assert str(exc_info.value) == "unauthorized"
    mock_sueno_repo.delete.assert_not_called()


def test_get_sueno_not_found_raises_value_error():
    """Verifica que solicitar un sueño que no existe lanza ValueError('dream_not_found')."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.get_sueno(sueno_id=999, usuario_actual_id=1)

    assert str(exc_info.value) == "dream_not_found"


def test_get_sueno_private_unauthorized_raises_permission_error():
    """Verifica que intentar ver un sueño privado ajeno lanza PermissionError('unauthorized')."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, publico=False, usuario_id=99
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(PermissionError) as exc_info:
        service.get_sueno(
            sueno_id=1, usuario_actual_id=1
        )  # El usuario 1 intenta ver el del usuario 99

    assert str(exc_info.value) == "unauthorized"


def test_get_sueno_success():
    """Verifica que se puede obtener un sueño existente y público correctamente."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, publico=True, usuario_id=1)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_sueno(sueno_id=1, usuario_actual_id=1)

    assert resultado.id == 1
    mock_sueno_repo.get_by_id.assert_called_once_with(1)


def test_create_sueno_title_too_long_raises_value_error():
    """Verifica que un título mayor a 100 caracteres lanza ValueError('title_too_long')."""
    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="A" * 101,
            contenido="Contenido válido para el sueño.",
            usuario_id=1,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "title_too_long"


def test_create_sueno_content_too_long_raises_value_error():
    """Verifica que un contenido mayor a 2000 caracteres lanza ValueError('content_too_long')."""
    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Título válido",
            contenido="A" * 2001,
            usuario_id=1,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "content_too_long"


def test_create_sueno_invalid_language_raises_value_error():
    """Verifica que un idioma original inválido lanza ValueError('invalid_language')."""
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = {"id": 1}

    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="Título válido",
            contenido="Contenido válido para el sueño.",
            usuario_id=1,
            categoria_id=1,
            idioma_original="fr",  # Idioma no soportado
            publico=True,
        )
    assert str(exc_info.value) == "invalid_language"


def test_update_sueno_not_found_raises_value_error():
    """Verifica que intentar actualizar un sueño que no existe lanza ValueError('dream_not_found')."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.update_sueno(
            sueno_id=999,
            titulo="Título válido",
            contenido="Contenido válido",
            categoria_id=1,
            publico=True,
            usuario_actual_id=1,
        )
    assert str(exc_info.value) == "dream_not_found"


def test_create_sueno_title_empty_raises_value_error():
    """Verifica que un título vacío o de solo espacios lanza ValueError('title_empty')."""
    mock_usuario_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_categoria_repo.get_by_id.return_value = {"id": 1}

    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=mock_usuario_repo,
        categoria_repository=mock_categoria_repo,
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_sueno(
            titulo="   ",  # Título vacío o solo espacios
            contenido="Contenido válido para el sueño.",
            usuario_id=1,
            categoria_id=1,
            idioma_original="es",
            publico=True,
        )
    assert str(exc_info.value) == "title_empty"


def test_get_sueno_detalles_success():
    """Verifica que se pueden obtener los detalles de un sueño público correctamente."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_detalles.return_value = MagicMock(
        id=1, publico=True, usuario_id=1
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_sueno_detalles(sueno_id=1, usuario_actual_id=1)

    assert resultado.id == 1
    mock_sueno_repo.get_detalles.assert_called_once_with(1, 1)


def test_get_sueno_detalles_private_unauthorized_raises_permission_error():
    """Verifica que intentar ver los detalles de un sueño privado ajeno lanza PermissionError."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_detalles.return_value = MagicMock(
        id=1, publico=False, usuario_id=99
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(PermissionError) as exc_info:
        service.get_sueno_detalles(sueno_id=1, usuario_actual_id=1)

    assert str(exc_info.value) == "unauthorized"


def test_update_sueno_with_hashtags_success():
    """Verifica que la actualización de un sueño limpia y reinserta correctamente los hashtags."""
    mock_sueno_repo = MagicMock()
    mock_hashtag_repo = MagicMock()

    # El sueño existe y pertenece al usuario 1
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1)
    mock_sueno_repo.update.return_value = {"id": 1, "titulo": "Actualizado"}

    # Simulamos que encuentra un hashtag existente y otro no (para forzar el insert)
    mock_hashtag_repo.get_by_nombre.side_effect = [
        MagicMock(id=10),  # El hashtag #nuevo ya existe
        None,  # El hashtag #extra no existe, creará uno nuevo
    ]
    mock_hashtag_repo.insert.return_value = MagicMock(id=11)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.update_sueno(
        sueno_id=1,
        titulo="Título con #nuevo",
        contenido="Contenido con #extra",
        categoria_id=1,
        publico=True,
        usuario_actual_id=1,
    )

    # Verificamos que se limpiaron las relaciones antiguas de hashtags
    mock_hashtag_repo.delete_relaciones_sueno.assert_called_once_with(1)
    # Verificamos que se insertaron las nuevas relaciones
    assert mock_hashtag_repo.insert_sueno_hashtag.call_count == 2


def test_get_sueno_detalles_not_found_raises_value_error():
    """Verifica que solicitar detalles de un sueño inexistente lanza ValueError('dream_not_found')."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_detalles.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.get_sueno_detalles(sueno_id=999, usuario_actual_id=1)

    assert str(exc_info.value) == "dream_not_found"


def test_get_user_suenos_success():
    """Verifica que se pueden obtener los sueños de un usuario existente correctamente."""
    mock_usuario_repo = MagicMock()
    mock_sueno_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_sueno_repo.get_feed_by_user.return_value = [{"id": 1}]

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_user_suenos(perfil_usuario_id=1, usuario_actual_id=1)
    assert len(resultado) == 1


def test_get_user_suenos_user_not_found_raises_value_error():
    """Verifica que consultar los sueños de un usuario inexistente lanza ValueError('user_does_not_exist')."""
    mock_usuario_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=MagicMock(),
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.get_user_suenos(perfil_usuario_id=999)

    assert str(exc_info.value) == "user_does_not_exist"


def test_get_feed_success():
    """Verifica que se puede obtener el feed general correctamente."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_feed_detalle.return_value = [{"id": 1}]

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_feed(usuario_id=1, page=1)
    assert len(resultado) == 1


def test_get_liked_suenos_success():
    """Verifica que se pueden obtener los sueños con 'like' de un usuario existente."""
    mock_usuario_repo = MagicMock()
    mock_sueno_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_sueno_repo.get_liked_by_user.return_value = [{"id": 1}]

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_liked_suenos(perfil_usuario_id=1, usuario_actual_id=1)
    assert len(resultado) == 1


def test_get_liked_suenos_user_not_found_raises_value_error():
    """Verifica que consultar los likes de un usuario inexistente lanza ValueError('user_does_not_exist')."""
    mock_usuario_repo = MagicMock()
    mock_sueno_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.get_liked_suenos(perfil_usuario_id=999)

    assert str(exc_info.value) == "user_does_not_exist"


def test_translate_sueno_cached_success():
    """Verifica que si ya existe una traducción en BD, se devuelve directamente."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, titulo="Original", contenido="Contenido", idioma_original="es"
    )
    # La traducción ya existe en la BD (devuelve tupla de 3 elementos)
    mock_sueno_repo.get_traduccion.return_value = (
        "en",
        "Cached Title",
        "Cached Content",
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.translate_sueno(sueno_id=1, idioma_destino="en")
    assert resultado["titulo"] == "Cached Title"
    mock_sueno_repo.get_traduccion.assert_called_once_with(1, "en")


def test_translate_sueno_new_translation_success():
    """Verifica que si no existe traducción, se traduce mediante el servicio y se guarda."""
    mock_sueno_repo = MagicMock()
    mock_translation_service = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, titulo="Original", contenido="Contenido", idioma_original="es"
    )
    mock_sueno_repo.get_traduccion.return_value = None
    mock_translation_service.translate.side_effect = [
        "Translated Title",
        "Translated Content",
    ]

    mock_sueno_repo.save_traduccion.return_value = (
        "en",
        "Translated Title",
        "Translated Content",
    )
    mock_sueno_repo.crear_preview.return_value = "Preview..."

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=mock_translation_service,
    )

    resultado = service.translate_sueno(sueno_id=1, idioma_destino="en")
    assert resultado["titulo"] == "Translated Title"
    mock_sueno_repo.save_traduccion.assert_called_once()


def test_get_liked_suenos_with_all_params():
    """Verifica get_liked_suenos pasando todos los filtros y parámetros opcionales."""
    mock_usuario_repo = MagicMock()
    mock_sueno_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_sueno_repo.get_liked_by_user.return_value = []

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    resultado = service.get_liked_suenos(
        perfil_usuario_id=1,
        usuario_actual_id=1,
        categorias=[1, 2],
        ordenar_por="fecha",
        direccion="desc",
    )
    assert resultado == []
    mock_sueno_repo.get_liked_by_user.assert_called_once_with(
        1, 1, [1, 2], "fecha", "desc"
    )


def test_update_sueno_hashtag_branch_coverage():
    """Cubre todas las ramas del bucle de hashtags en update_sueno (existente y nuevo)."""
    mock_sueno_repo = MagicMock()
    mock_hashtag_repo = MagicMock()

    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1)
    mock_sueno_repo.update.return_value = {"id": 1}

    # Creamos objetos simulados que tengan la propiedad .id accesible mediante punto
    hashtag_existente = MagicMock(id=10)
    hashtag_nuevo = MagicMock(id=11)

    # Simulamos que el hashtag 'amor' ya existe y 'aventura' devuelve None (para que se inserte)
    mock_hashtag_repo.get_by_nombre.side_effect = lambda nombre: (
        hashtag_existente if nombre == "amor" else None
    )
    mock_hashtag_repo.insert.return_value = hashtag_nuevo

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.update_sueno(
        sueno_id=1,
        titulo="Título",
        contenido="#amor y #aventura",
        categoria_id=1,
        publico=True,
        usuario_actual_id=1,
    )

    # Verificamos que intentó buscar ambos y crear el que faltaba
    assert mock_hashtag_repo.get_by_nombre.call_count == 2
    mock_hashtag_repo.insert.assert_called_once()


def test_get_liked_suenos_default_params():
    """Cubre las líneas de parámetros por defecto en get_liked_suenos."""
    mock_usuario_repo = MagicMock()
    mock_sueno_repo = MagicMock()
    mock_usuario_repo.get_by_id.return_value = {"id": 1}
    mock_sueno_repo.get_liked_by_user.return_value = []

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=mock_usuario_repo,
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    service.get_liked_suenos(perfil_usuario_id=1, usuario_actual_id=1)

    mock_sueno_repo.get_liked_by_user.assert_called_once_with(1, 1, None, None, None)


def test_update_sueno_hashtag_insert_branch():
    """Cubre específicamente la rama donde el hashtag no existe y se inserta en update_sueno."""
    mock_sueno_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True)
    mock_sueno_repo.update.return_value = {"id": 1}
    
    # Forzamos que get_by_nombre devuelva None para que entre al if y llame a insert
    mock_hashtag_repo.get_by_nombre.return_value = None
    mock_hashtag_repo.insert.return_value = MagicMock(id=99)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.update_sueno(
        sueno_id=1,
        titulo="Título con #nuevo",
        contenido="Contenido",
        categoria_id=1,
        publico=True,
        usuario_actual_id=1,
    )

    mock_hashtag_repo.insert.assert_called_once()


def test_translate_sueno_invalid_language_branch():
    """Cubre la línea exacta de idioma inválido en translate_sueno."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True, idioma_original="es")

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.translate_sueno(sueno_id=1, idioma_destino="xx", usuario_actual_id=1)
    
    assert str(exc_info.value) == "invalid_language"


def test_translate_sueno_same_language_branch():
    """Cubre la línea exacta de mismo idioma en translate_sueno."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True, idioma_original="es")

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc_info:
        service.translate_sueno(sueno_id=1, idioma_destino="es", usuario_actual_id=1)
    
    assert str(exc_info.value) == "same_language"
    
def test_update_sueno_hashtag_loop_complete():
    """Cubre las líneas 91 a 108 del bucle de hashtags en update_sueno."""
    mock_sueno_repo = MagicMock()
    mock_hashtag_repo = MagicMock()
    
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True)
    mock_sueno_repo.update.return_value = {"id": 1}
    
    mock_hashtag_repo.get_by_nombre.side_effect = lambda n: (
        MagicMock(id=10) if n == "existente" else None
    )
    mock_hashtag_repo.insert.return_value = MagicMock(id=20)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=mock_hashtag_repo,
        translation_service=MagicMock(),
    )

    service.update_sueno(
        sueno_id=1,
        titulo="Sueño con #existente",
        contenido="y con #nuevo",
        categoria_id=1,
        publico=True,
        usuario_actual_id=1,
    )

    assert mock_hashtag_repo.get_by_nombre.call_count == 2
    assert mock_hashtag_repo.insert.call_count == 1


def test_translate_sueno_invalid_language_line():
    """Cubre la línea 223 de idioma inválido en translate_sueno."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True, idioma_original="es")

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc:
        service.translate_sueno(sueno_id=1, idioma_destino="invalido", usuario_actual_id=1)
    assert str(exc.value) == "invalid_language"


def test_translate_sueno_same_language_line():
    """Cubre la línea 227 de mismo idioma en translate_sueno."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1, publico=True, idioma_original="es")

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc:
        service.translate_sueno(sueno_id=1, idioma_destino="es", usuario_actual_id=1)
    assert str(exc.value) == "same_language"
    
def test_update_sueno_validations_raises_errors():
    """Cubre todas las validaciones de título y contenido en update_sueno (líneas 91-108)."""
    mock_sueno_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1)
    mock_categoria_repo.get_by_id.return_value = MagicMock(id=1)

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=mock_categoria_repo,
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    # 1. Título vacío
    with pytest.raises(ValueError, match="title_empty"):
        service.update_sueno(1, "", "Contenido válido", 1, True, 1)

    # 2. Título muy corto (< 3)
    with pytest.raises(ValueError, match="title_too_short"):
        service.update_sueno(1, "Hi", "Contenido válido", 1, True, 1)

    # 3. Título muy largo (> 100)
    with pytest.raises(ValueError, match="title_too_long"):
        service.update_sueno(1, "A" * 101, "Contenido válido", 1, True, 1)

    # 4. Contenido muy corto (< 5)
    with pytest.raises(ValueError, match="content_too_short"):
        service.update_sueno(1, "Título válido", "Hola", 1, True, 1)

    # 5. Contenido muy largo (> 2000)
    with pytest.raises(ValueError, match="content_too_long"):
        service.update_sueno(1, "Título válido", "A" * 2001, 1, True, 1)


def test_translate_sueno_unauthorized_permission_error():
    """Cubre el error de permisos en translate_sueno para sueños privados (líneas 223-227)."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = MagicMock(
        id=1, 
        usuario_id=2, 
        publico=False, 
        idioma_original="es"
    )

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(PermissionError) as exc:
        service.translate_sueno(sueno_id=1, idioma_destino="en", usuario_actual_id=1)
    
    assert str(exc.value) == "unauthorized"
    
def test_update_sueno_category_not_found():
    """Cubre la línea 91: error cuando la categoría no existe en update_sueno."""
    mock_sueno_repo = MagicMock()
    mock_categoria_repo = MagicMock()
    
    mock_sueno_repo.get_by_id.return_value = MagicMock(id=1, usuario_id=1)
    mock_categoria_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=mock_categoria_repo,
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc:
        service.update_sueno(
            sueno_id=1,
            titulo="Título válido",
            contenido="Contenido válido",
            categoria_id=999,
            publico=True,
            usuario_actual_id=1,
        )
    assert str(exc.value) == "category_not_found"


def test_translate_sueno_dream_not_found():
    """Cubre la línea 223: error cuando el sueño no existe en translate_sueno."""
    mock_sueno_repo = MagicMock()
    mock_sueno_repo.get_by_id.return_value = None

    service = SuenoService(
        sueno_repository=mock_sueno_repo,
        usuario_repository=MagicMock(),
        categoria_repository=MagicMock(),
        hashtag_repository=MagicMock(),
        translation_service=MagicMock(),
    )

    with pytest.raises(ValueError) as exc:
        service.translate_sueno(sueno_id=999, idioma_destino="en")
    assert str(exc.value) == "dream_not_found"