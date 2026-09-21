import { useEffect, useState } from "react"
import { useParams, useLocation, useNavigate } from "react-router-dom"

import { getSuenoDetalle, updateSueno, deleteSueno, toggleLike } from "../api/suenos"
import {
    getComentarios,
    createComentario,
    deleteComentario,
    updateComentario
} from "../api/comentarios"
import { getCategorias } from "../api/categorias"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"

import ConfirmModal from "../components/ConfirmModal"
import HashtagText from "../components/HashtagText"
import {
    Globe,
    Heart,
    MessageCircle,
    Pencil,
    Trash2,
    Lock,
    Tag
} from "../lib/icons"
import Avatar from "../components/Avatar"

function SuenoDetallePage() {
    // useParams obtiene el id de la URL
    const { id } = useParams()
    const { user } = useAuth()
    const { showToast } = useToast()
    const location = useLocation()

    const [sueno, setSueno] = useState(null)
    const [categorias, setCategorias] = useState([])
    const [categoriaId, setCategoriaId] = useState(null)

    const [comentarios, setComentarios] = useState([])
    const [nuevoComentario, setNuevoComentario] = useState("")
    const [nuevoId, setNuevoId] = useState(null)

    const [tituloEdit, setTituloEdit] = useState("")
    const [contenidoEdit, setContenidoEdit] = useState("")
    const [publicoEdit, setPublicoEdit] = useState(true)
    const [editando, setEditando] = useState(false)
    const [editFromFeed, setEditFromFeed] = useState(false)

    const [liked, setLiked] = useState(false)
    const [likeAnimating, setLikeAnimating] = useState(false)

    const [comentarioEditandoId, setComentarioEditandoId] = useState(null)
    const [contenidoEditComentario, setContenidoEditComentario] = useState("")

    const [confirmandoBorrado, setConfirmandoBorrado] = useState(false)
    const [comentarioAEliminar, setComentarioAEliminar] = useState(null)

    const [loading, setLoading] = useState(true)
    const [savingEdit, setSavingEdit] = useState(false)
    const [deleting, setDeleting] = useState(false)
    const [commenting, setCommenting] = useState(false)
    const [loadingLike, setLoadingLike] = useState(false)
    const [deletingComentario, setDeletingComentario] = useState(false)
    const [savingComentario, setSavingComentario] = useState(false)

    const [error, setError] = useState("")
    const navigate = useNavigate()

    useEffect(() => {
        async function loadData() {
            try {
                const suenoData = await getSuenoDetalle(id)
                const categoriasData = await getCategorias()
                const comentariosData = await getComentarios(id)

                setSueno(suenoData)
                setLiked(suenoData.liked_by_user)
                setCategorias(categoriasData)
                setComentarios(comentariosData)
            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
            }
        }

        loadData()
    }, [id])

    // Limpiar comentario
    useEffect(() => {
        if (!nuevoId) return

        const timer = setTimeout(() => {
            setNuevoId(null)
        }, 2000)

        return () => clearTimeout(timer)
    }, [nuevoId])

    //Edición desde Feed
    useEffect(() => {
        if (location.state?.editar && sueno && !editFromFeed) {
            setEditando(true)
            setTituloEdit(sueno.titulo)
            setCategoriaId(sueno.categoria_id)
            setContenidoEdit(sueno.contenido)
            setPublicoEdit(sueno.publico)
            setEditFromFeed(true)
            //Limpia del state para evitar el modo al recargar
            window.history.replaceState({}, document.title)
        }
    }, [location.state, sueno, editFromFeed])

    // Manejo del like
    async function handleLike() {
        if (loadingLike) return

        if (!user) {
            showToast("Debes iniciar sesión", "error")
            return
        }

        setLoadingLike(true)

        try {
            const data = await toggleLike(sueno.id)

            setSueno(prev => ({
                ...prev,
                likes_count: data.likes_count
            }))

            setLiked(data.status === "liked")

            if (data.status === "liked") {
                setLikeAnimating(true)
                setTimeout(() => setLikeAnimating(false), 250)
            }

            showToast(
                data.status === "liked"
                    ? "Like añadido"
                    : "Like eliminado",
                "success"
            )

        } catch (err) {
            showToast("Error al dar like", "error")
        } finally {
            setLoadingLike(false)
        }
    }

    async function handleCrearComentario() {
        if (commenting) return

        if (!user) {
            setError("Debes iniciar sesión para comentar")
            showToast("Debes iniciar sesión", "error")
            return
        }

        if (!nuevoComentario.trim()) {
            setError("Escribe algo antes de comentar")
            return
        }
        setCommenting(true)

        try {
            const nuevo = await createComentario(id, nuevoComentario)

            showToast("Comentario añadido", "success")

            setComentarios((prev) => [...prev, nuevo])
            setNuevoId(nuevo.id)
            setNuevoComentario("")

            setTimeout(() => {
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: "smooth"
                })
            }, 100)
        }
        catch (err) {
            setError(err.message)
            showToast("Error al comentar", "error")
        } finally {
            setCommenting(false)
        }
    }


    // Editar Sueño
    async function handleGuardar() {
        if (savingEdit) return

        if (!tituloEdit.trim()) {
            setError("El título no puede estar vacío")
            return
        }

        if (tituloEdit.trim().length < 3) {
            setError("El título debe tener al menos 3 caracteres")
            return
        }

        if (contenidoEdit.trim().length < 5) {
            setError("El contenido debe tener al menos 5 caracteres")
            return
        }

        setSavingEdit(true)

        try {
            await updateSueno(sueno.id, {
                titulo: tituloEdit,
                contenido: contenidoEdit,
                publico: publicoEdit,
                categoria_id: categoriaId
            })

            const suenoActualizado = await getSuenoDetalle(id)

            showToast("Sueño actualizado", "success")

            setSueno(suenoActualizado)
            setEditando(false)

        } catch (err) {
            setError(err.message)
            showToast("Error al editar sueño", "error")
        } finally {
            setSavingEdit(false)
        }
    }


    // Borrar Sueño
    async function handleDelete() {
        if (deleting) return

        setDeleting(true)

        try {
            await deleteSueno(id)
            showToast("Sueño eliminado", "success")
            navigate("/home")
        } catch (err) {
            setError(err.message)
            showToast("Error al eliminar", "error")
        } finally {
            setDeleting(false)
        }
    }

    // Editar Comentario

    async function handleEditarComentario(comentarioId) {
        if (savingComentario) return

        if (!contenidoEditComentario.trim()) {
            showToast("Comentario vacío", "error")
            return
        }

        setSavingComentario(true)

        try {
            const actualizado =
                await updateComentario(
                    comentarioId,
                    contenidoEditComentario
                )
            setComentarios(prev =>
                prev.map(c =>
                    c.id === comentarioId ? actualizado : c
                )
            )

            setComentarioEditandoId(null)
            setContenidoEditComentario("")

            showToast("Comentario actualizado", "success")

        } catch (err) {
            showToast("Error al editar comentario", "error")
        } finally {
            setSavingComentario(false)
        }
    }

    // Borrar Comentario
    async function handleDeleteComentario() {
        if (!comentarioAEliminar || deletingComentario) return

        setDeletingComentario(true)

        try {
            await deleteComentario(comentarioAEliminar)

            setComentarios(prev =>
                prev.filter(c => c.id !== comentarioAEliminar)
            )

            showToast("Comentario eliminado", "success")

            setComentarioAEliminar(null)

        } catch (err) {
            setError(err.message)
            showToast("Error al eliminar comentario", "error")
        } finally {
            setDeletingComentario(false)
        }
    }

    if (loading) {
        return (
            <p className="sueno-detalle-loading">
                Cargando sueño...
            </p>
        )
    }

    if (!sueno) {
        return (
            <p className="sueno-detalle-empty">
                No encontrado
            </p>
        )
    }

    const fechaFormateada = new Date(sueno.fecha_creacion).toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    })

    return (

        <div className="sueno-detalle-page">

            {error && (
                <p className="sueno-detalle-error">
                    {error}
                </p>
            )}
            <div className="sueno-detalle-card">

                {editando ? (
                    <div className="sueno-edit-card">
                        <input
                            className="input sueno-edit-input"
                            value={tituloEdit}
                            onChange={(e) => {
                                setTituloEdit(e.target.value)
                                setError("")
                            }
                            }
                        />

                        <select
                            className="select sueno-edit-select"
                            value={categoriaId}
                            onChange={(e) => setCategoriaId(Number(e.target.value))}
                        >
                            {!categoriaId && <option value="">Selecciona categoría</option>}
                            {categorias.map(c => (
                                <option key={c.id} value={c.id}>
                                    {c.nombre}
                                </option>
                            ))}
                        </select>

                        <textarea
                            className="textarea sueno-edit-textarea"
                            value={contenidoEdit}
                            onChange={(e) => {
                                setContenidoEdit(e.target.value)
                                setError("")
                            }}
                        />

                        <div className="sueno-edit-visibility">
                            <label>
                                <input
                                    type="checkbox"
                                    checked={publicoEdit}
                                    onChange={(e) => setPublicoEdit(e.target.checked)}
                                />

                                {" "}
                                Hacer público
                            </label>
                        </div>

                        <div className="sueno-edit-actions">
                            <button
                                className="btn btn-primary"
                                onClick={handleGuardar}
                                disabled={savingEdit}>
                                {savingEdit ? "Guardando..." : "Guardar"}
                            </button>

                            <button
                                className="btn btn-secondary"
                                onClick={() => setEditando(false)}>
                                Cancelar
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="sueno-detalle-content">

                        <div className="sueno-detalle-author-section">
                            <Avatar
                                avatarUrl={sueno.avatar_url}
                                nombre={sueno.usuario_nombre}
                                usuarioId={sueno.usuario_id}
                            />

                            <span className="sueno-detalle-author">
                                {sueno.usuario_nombre}
                            </span>

                        </div>

                        <h2 className="sueno-detalle-title">
                            <HashtagText texto={sueno.titulo} />
                        </h2>

                        <div className="sueno-detalle-details">

                            <p className="sueno-detalle-category">
                                <Tag size={14} />
                                <span>{sueno.categoria_nombre}</span>
                            </p>

                            {user?.id === sueno.usuario_id && (
                                <span className={`sueno-detalle-visibility ${sueno.publico ? "is-public" : "is-private"}`}>
                                    {sueno.publico ? (
                                        <>
                                            <Globe size={14} />
                                            <span>Público</span>
                                        </>
                                    ) : (
                                        <>
                                            <Lock size={14} />
                                            <span>Privado</span>
                                        </>
                                    )}
                                </span>
                            )}
                        </div>

                        <p className="sueno-detalle-text">
                            <HashtagText texto={sueno.contenido} />
                        </p>
                    </div>

                )}

                <div className="sueno-detalle-meta">
                    <div className="sueno-detalle-stats">
                        <button
                            className={`sueno-like-button ${liked ? "is-liked" : ""} ${likeAnimating ? "is-animating" : ""}`} onClick={handleLike}
                            disabled={loadingLike}
                        >
                            <Heart size={18} />
                            <span>
                                {loadingLike ? "..." : sueno.likes_count}
                            </span>
                        </button>

                        <span>
                            <MessageCircle size={18} />
                            {sueno.comentarios_count}
                        </span>
                    </div>

                    <div className="sueno-detalle-date">
                        {fechaFormateada}
                    </div>
                </div>

                {/* Acciones propietario */}
                {!editando && user?.id === sueno.usuario_id && (
                    <div className="sueno-detalle-owner-actions">

                        {/* Botón Editar */}
                        <button
                            className="sueno-owner-button"
                            onClick={() => {
                                setEditando(true)
                                setTituloEdit(sueno.titulo)
                                setCategoriaId(sueno.categoria_id)
                                setContenidoEdit(sueno.contenido)
                                setPublicoEdit(sueno.publico)
                            }}
                        >
                            <Pencil size={14} />
                            Editar
                        </button>


                        {/* Botón eliminar */}
                        <button
                            className="sueno-owner-button"
                            onClick={() => setConfirmandoBorrado(true)}
                            disabled={deleting}
                        >
                            <Trash2 size={14} />
                            {deleting ? "Eliminando..." : "Eliminar"}
                        </button>
                    </div>
                )}
            </div>

            {/* Comentarios */}

            <section className="sueno-detalle-comments">


                <h3 className="sueno-detalle-comments-title">
                    Comentarios
                </h3>

                <div className="sueno-detalle-comment-form">
                    <textarea
                        className=" textarea sueno-detalle-comment-input"
                        value={nuevoComentario}
                        onChange={(e) => setNuevoComentario(e.target.value)}
                        placeholder="Escribe un comentario..."
                        disabled={commenting}
                    />

                    <button
                        className="btn btn-primary"
                        onClick={handleCrearComentario}
                        disabled={commenting || !nuevoComentario.trim()}
                    >
                        {commenting ? "Comentando..." : "Comentar"}
                    </button>
                </div>
                <div className="sueno-detalle-comments-list">
                    {comentarios.map((c) => (
                        <div
                            key={c.id}
                            className={`comentario ${c.id === nuevoId ? "is-new" : ""}`}
                        >
                            {/* Avatar */}
                            <Avatar
                                avatarUrl={c.avatar_url}
                                nombre={c.usuario_nombre}
                                usuarioId={c.usuario_id}
                                size={36}
                            />

                            {/* Texto */}
                            <div className="comentario-content">

                                <div className="comentario-header">
                                    <strong>{c.usuario_nombre}</strong>

                                    {/* Editar comentario */}
                                    {user?.id === c.usuario_id && (
                                        <button
                                            className="comentario-action"
                                            onClick={() => {
                                                setComentarioEditandoId(c.id)
                                                setContenidoEditComentario(c.contenido)
                                            }}
                                        >
                                            Editar
                                        </button>
                                    )}

                                    {/* Eliminar comentario */}
                                    {(user?.id === c.usuario_id ||
                                        user?.id === sueno.usuario_id) && (
                                            <button
                                                className="comentario-action"
                                                onClick={() =>
                                                    setComentarioAEliminar(c.id)
                                                }
                                            >
                                                Eliminar
                                            </button>
                                        )}

                                    <span className="comentario-date">
                                        {new Date(c.fecha_creacion).toLocaleString("es-ES", {
                                            day: "2-digit",
                                            month: "2-digit",
                                            year: "2-digit",
                                            hour: "2-digit",
                                            minute: "2-digit"
                                        })}
                                    </span>

                                </div>

                                {comentarioEditandoId === c.id ? (
                                    <>
                                        <textarea
                                            className="textarea comentario-edit-input"
                                            value={contenidoEditComentario}
                                            onChange={(e) =>
                                                setContenidoEditComentario(
                                                    e.target.value
                                                )
                                            }
                                        />

                                        <div className="comentario-edit-actions">
                                            <button
                                                className="btn btn-primary"
                                                onClick={() => handleEditarComentario(c.id)}
                                                disabled={savingComentario}
                                            >
                                                {savingComentario ? "Guardando..." : "Guardar"}
                                            </button>

                                            <button
                                                className="btn btn-secondary"
                                                onClick={() => {
                                                    setComentarioEditandoId(null)
                                                    setContenidoEditComentario("")
                                                }}
                                            >
                                                Cancelar
                                            </button>
                                        </div>
                                    </>
                                ) : (
                                    <p className="comentario-text">
                                        {c.contenido}
                                    </p>
                                )}
                            </div>
                        </div>
                    ))}

                    <ConfirmModal
                        open={comentarioAEliminar !== null}
                        title="¿Eliminar comentario?"
                        message="Esta acción no se puede deshacer."
                        confirmText="Borrar"
                        loading={deletingComentario}
                        onConfirm={handleDeleteComentario}
                        onCancel={() => setComentarioAEliminar(null)}
                    />
                </div>
            </section>

            <ConfirmModal
                open={confirmandoBorrado}
                title="¿Eliminar sueño?"
                message="Esta acción no se puede deshacer."
                confirmText="Borrar"
                onConfirm={handleDelete}
                onCancel={() => setConfirmandoBorrado(false)}
            />

        </div>

    )

}

export default SuenoDetallePage