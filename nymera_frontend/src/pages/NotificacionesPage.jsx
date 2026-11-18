import { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"
import { getNotificaciones, marcarNotificacionLeida, marcarTodasComoLeidas } from "../api/notificaciones"
import { Link } from "react-router-dom"
import { useToast } from "../context/ToastContext"

import SEO from "../components/SEO"

import { formatDate } from "../utils/formatDate"

import { Heart, MessageCircle } from "../lib/icons"

function NotificacionesPage() {
    const { t, i18n } = useTranslation()

    const [notificaciones, setNotificaciones] = useState([])
    const [loading, setLoading] = useState(true)
    const[markingAll, setMarkingAll] = useState(false)
    const { showToast } = useToast()

    useEffect(() => {
        async function load() {
            try {
                const data = await getNotificaciones()
                setNotificaciones(data)
            } catch (err) {
                showToast(t("notifications.loadError"), "error")
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    async function handleMarcarTodas() {
        if (markingAll) return
        setMarkingAll(true)

        try {
            await marcarTodasComoLeidas()
            setNotificaciones(prev =>
                prev.map(notif => ({ ...notif, leido: true }))
            )
            window.dispatchEvent(new CustomEvent("notificacionesActualizadas", { detail: { count: 0 } }))

            showToast(t("notifications.allMarkedReadSuccess"), "success")
        } catch (err) {
            showToast(t("notifications.markAllReadError"), "error")
        } finally {
            setMarkingAll(false)
        }
    }

    const hayNoLeidas = notificaciones.some(n => !n.leido)

    return (
        <div className="notificaciones-page">
            <SEO
                title={t('seo.notificaciones.title')}
                description={t('seo.notificaciones.description')}
            />

            <div className="notificaciones-header">
                <h1 className="notificaciones-title">
                    {t("notifications.title")}
                </h1>

                {!loading && notificaciones.length > 0 && hayNoLeidas && (
                    <button
                        type="button"
                        onClick={handleMarcarTodas}
                        className="sueno-owner-button"
                        disabled={markingAll}
                    >
                        {t("notifications.markAllAsRead")}
                    </button>
                )}
            </div>

            {loading ? (
                <p className="notificaciones-loading" role="status" aria-live="polite" >
                    {t("notifications.loading")}
                </p>
            ) : notificaciones.length === 0 ? (
                <p className="notificaciones-empty">
                    {t("notifications.empty")}
                </p>
            ) : (
                <div className="notificaciones-list">
                    {notificaciones.map((n) => (
                        <Link
                            key={n.id}
                            to={`/suenos/${n.sueno_id}`}
                            className={`notificacion ${n.leido ? "is-read" : ""}`}
                            aria-label={t(n.leido ? "accessibility.readNotification" : "accessibility.unreadNotification", { name: n.emisor_nombre })}
                            onClick={async () => {
                                if (!n.leido) {
                                    try {
                                        await marcarNotificacionLeida(n.id)
                                        setNotificaciones(prev =>
                                            prev.map(notif =>
                                                notif.id === n.id
                                                    ? { ...notif, leido: true }
                                                    : notif
                                            )
                                        )
                                        const nuevasNoLeidas = notificaciones.filter(notif => notif.id !== n.id && !notif.leido).length
                                        window.dispatchEvent(new CustomEvent("notificacionesActualizadas", { detail: { count: nuevasNoLeidas } }))
                                    } catch (err) {
                                        showToast(t("notifications.markReadError"), "error")
                                    }
                                }
                            }}
                        >
                            <div className="notificacion-content">
                                {n.tipo === "like" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> {t("notifications.like")}{" "}
                                        <Heart size={16} aria-hidden="true" />
                                    </p>
                                )}

                                {n.tipo === "comentario" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> {t("notifications.comment")}{" "}
                                        <MessageCircle size={16} aria-hidden="true" />
                                    </p>
                                )}

                                <span className="notificacion-date">
                                    {formatDate(n.fecha_creacion, i18n.language)}
                                </span>
                            </div>
                        </Link>
                    ))}
                </div>
            )
            }
        </div >
    )
}

export default NotificacionesPage