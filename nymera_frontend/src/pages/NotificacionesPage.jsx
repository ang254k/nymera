import { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"
import { getNotificaciones, marcarNotificacionLeida } from "../api/notificaciones"
import { useNavigate } from "react-router-dom"
import { useToast } from "../context/ToastContext"

import SEO from "../components/SEO"

import { formatDate } from "../utils/formatDate"

import { Heart, MessageCircle } from "../lib/icons"

function NotificacionesPage() {
    const { t, i18n } = useTranslation()

    const [notificaciones, setNotificaciones] = useState([])
    const [loading, setLoading] = useState(true)
    const { showToast } = useToast()

    const navigate = useNavigate()

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

    return (
        <div className="notificaciones-page">
            <SEO
                title={t('seo.notificaciones.title')}
                description={t('seo.notificaciones.description')}
            />

            <h1 className="notificaciones-title">
                {t("notifications.title")}
            </h1>

            {loading ? (
                <p className="notificaciones-loading" >
                    {t("notifications.loading")}
                </p>
            ) : notificaciones.length === 0 ? (
                <p className="notificaciones-empty">
                    {t("notifications.empty")}
                </p>
            ) : (
                <div className="notificaciones-list">
                    {notificaciones.map((n) => (
                        <div
                            key={n.id}
                            className={`notificacion ${n.leido ? "is-read" : ""}`}
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
                                    } catch (err) {
                                        showToast(t("notifications.markReadError"), "error")
                                    }
                                }
                                navigate(`/suenos/${n.sueno_id}`)
                            }}
                        >
                            <div className="notificacion-content">
                                {n.tipo === "like" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> {t("notifications.like")}{" "}
                                        <Heart size={16} />
                                    </p>
                                )}

                                {n.tipo === "comentario" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> {t("notifications.comment")}{" "}
                                        <MessageCircle size={16} />
                                    </p>
                                )}

                                <span className="notificacion-date">
                                    {formatDate(n.fecha_creacion, i18n.language)}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )
            }
        </div >
    )
}

export default NotificacionesPage