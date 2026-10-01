import { useState } from "react"
import { useTranslation } from "react-i18next"
import { useNavigate } from "react-router-dom"
import { deleteSueno, toggleLike } from "../api/suenos"
import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"
import { formatDate } from "../utils/formatDate"
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
    const { t, i18n } = useTranslation()

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
            showToast(t("dreamCard.loginRequired"), "error")
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
                data.status === "liked"
                    ? t("dreamCard.likeAdded")
                    : t("dreamCard.likeRemoved"),
                "success"
            )

        } catch (err) {
            showToast(t("dreamCard.likeError"), "error")
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

            showToast(t("dreamCard.deleted"), "success")

            setShowDeleteModal(false)
        } catch (err) {
            showToast(t("dreamCard.deleteError"), "error")
        } finally {
            setDeleting(false)
        }
    }

    const fechaFormateada = formatDate(
        sueno.fecha_creacion,
        i18n.language
    )

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
                                        <span>{t("dreamCard.public")}</span>
                                    </>
                                ) : (
                                    <>
                                        <Lock size={14} />
                                        <span>{t("dreamCard.private")}</span> </>
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
                                    {t("dreamCard.edit")}
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
                                    {deleting ? t("dreamCard.deleting") : t("dreamCard.delete")}
                                </button>
                            </div>
                        )}
                    </div>

                </div>

            </div>

            <ConfirmModal
                open={showDeleteModal}
                title={t("dreamCard.deleteTitle")}
                message={t("dreamCard.deleteMessage")}
                confirmText={
                    deleting
                        ? t("dreamCard.deleting")
                        : t("dreamCard.delete")
                }
                loadingText={t("dreamCard.deleting")}
                cancelText={t("dreamCard.cancel")}
                onConfirm={handleDelete}
                onCancel={() => setShowDeleteModal(false)}
                loading={deleting}
            />
        </>
    )
}

export default SuenoCard