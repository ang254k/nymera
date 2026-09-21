import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { deleteSueno, toggleLike } from "../api/suenos"
import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"
import {
    Heart,
    MessageCircle,
    Pencil,
    Trash2,
    Tag,
    Globe,
    Lock
} from "../lib/icons"

import ConfirmModal from "./ConfirmModal"
import HashtagText from "./HashtagText"
import Avatar from "./Avatar"

function SuenoCard({ sueno, onSuenoEliminado }) {
    const navigate = useNavigate()

    const [likesCount, setLikesCount] = useState(sueno.likes_count)
    const [liked, setLiked] = useState(sueno.liked_by_user)
    const [loadingLike, setLoadingLike] = useState(false)
    const [deleting, setDeleting] = useState(false)
    const [showDeleteModal, setShowDeleteModal] = useState(false)
    const [likeAnimating, setLikeAnimating] = useState(false)

    const { user } = useAuth()
    const { showToast } = useToast()


    // Like
    async function handleLike(e) {
        e.stopPropagation()
        if (loadingLike) return

        if (!user) {
            showToast("Debes iniciar sesión", "error")
            return
        }

        setLoadingLike(true)

        try {

            const data = await toggleLike(sueno.id)

            setLikesCount(data.likes_count)
            setLiked(data.status === "liked")
            if (data.status === "liked") {
                setLikeAnimating(true)
                setTimeout(() => setLikeAnimating(false), 250)
            }

            showToast(
                data.status === "liked" ? "Like añadido" : "Like eliminado",
                "success"
            )

        } catch (err) {
            showToast("Error al dar like", "error")
        } finally {
            setLoadingLike(false)
        }
    }

    // Borrar Sueno
    async function handleDelete() {
        if (deleting) return

        setDeleting(true)

        try {
            await deleteSueno(sueno.id)
            onSuenoEliminado(sueno.id)

            showToast("Sueño eliminado", "success")

            setShowDeleteModal(false)
        } catch (err) {
            showToast("Error al eliminar", "error")
        } finally {
            setDeleting(false)
        }
    }

    const fechaFormateada = new Date(sueno.fecha_creacion).toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });

    return (
        <>
            <div className="sueno-card">

                {/*Contenido clickable*/}
                <div
                    className="sueno-card-body"
                    onClick={() => {
                        const seleccion = window.getSelection()?.toString()
                        if (seleccion) return

                        navigate(`/suenos/${sueno.id}`)
                    }}
                >
                    {/* Avatar + nombre */}
                    <div className="sueno-author-section">
                        <Avatar
                            avatarUrl={sueno.avatar_url}
                            nombre={sueno.usuario_nombre}
                            usuarioId={sueno.usuario_id}
                        />

                        <span
                            onClick={(e) => {
                                e.stopPropagation()
                                navigate(`/usuarios/${sueno.usuario_id}`)
                            }}
                            className="sueno-author"
                        >
                            {sueno.usuario_nombre}
                        </span>
                    </div>


                    <h3 className="sueno-title">
                        <HashtagText texto={sueno.titulo} />
                    </h3>
                    <div className="sueno-details">
                        <p className="sueno-category">
                            <Tag size={14} />
                            <span>{sueno.categoria_nombre}</span>
                        </p>

                        {user?.id === sueno.usuario_id && (
                            <span
                                className={`sueno-visibility ${sueno.publico ? "is-public" : "is-private"
                                    }`}>
                                {sueno.publico ? (
                                    <>
                                        <Globe size={14} />
                                        <span>Público</span>
                                    </>
                                ) : (
                                    <>
                                        <Lock size={14} />
                                        <span>Privado</span> </>
                                )}
                            </span>
                        )}
                    </div>

                    <p className="sueno-preview">
                        <HashtagText texto={sueno.preview_contenido} />
                    </p>
                </div>

                {/* Footer */}
                <div className="sueno-card-footer">
                    {/* Izquierda: acciones */}
                    <div className="sueno-actions">
                        <button
                            className={`sueno-like-button ${liked ? "is-liked" : ""} ${likeAnimating ? "is-animating" : ""}`}
                            onClick={handleLike}
                            disabled={loadingLike}
                        >
                            <Heart size={18} />
                            <span>{loadingLike ? "..." : likesCount}</span>
                        </button>
                        <span className="sueno-comments">
                            <MessageCircle size={18} />
                            <span>{sueno.comentarios_count}</span>
                        </span>
                    </div>

                    {/* Derecha: fecha + delete */}
                    <div className="sueno-meta">
                        <div className="sueno-date">
                            {fechaFormateada}
                        </div>

                        {/* Acciones propietario (Borrar + Editar) */}
                        {user && user.id === sueno.usuario_id && (
                            <div className="sueno-owner-actions">
                                <button
                                    className="sueno-owner-button"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        navigate(`/suenos/${sueno.id}`, {
                                            state: { editar: true }
                                        })
                                    }}
                                >
                                    <Pencil size={14} />
                                    Editar
                                </button>

                                <button
                                    className="sueno-owner-button"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        setShowDeleteModal(true)
                                    }}
                                    disabled={deleting}
                                >
                                    <Trash2 size={14} />
                                    {deleting ? "Eliminando..." : "Eliminar"}
                                </button>
                            </div>
                        )}
                    </div>

                </div>

            </div>

            <ConfirmModal
                open={showDeleteModal}
                title="Eliminar sueño"
                message="¿Estás seguro de que quieres eliminar este sueño? Esta acción no se puede deshacer."
                confirmText={deleting ? "Eliminando..." : "Eliminar"}
                onConfirm={handleDelete}
                onCancel={() => setShowDeleteModal(false)}
                loading={deleting}
            />
        </>
    )
}

export default SuenoCard