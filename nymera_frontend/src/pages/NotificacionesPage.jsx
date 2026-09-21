import { useEffect, useState } from "react"
import { getNotificaciones, marcarNotificacionLeida } from "../api/notificaciones"
import { useNavigate } from "react-router-dom"
import { useToast } from "../context/ToastContext"

import { Heart, MessageCircle } from "../lib/icons"

function NotificacionesPage() {
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
                showToast("Error cargando notificaciones", "error")
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    if (loading) {
        return (
            <p className="notificaciones-loading">
                Cargando notificaciones...
            </p>
        )
    }


    return (
        <div className="notificaciones-page">
            <h1 className="notificaciones-title">
                Notificaciones
            </h1>

            {notificaciones.length === 0 ? (
                <p className="notificaciones-empty">
                    No tienes notificaciones
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
                                        showToast("No se pudo marcar la notificación como leída", "error")
                                    }
                                }
                                navigate(`/suenos/${n.sueno_id}`)
                            }}
                        >
                            <div className="notificacion-content">
                                {n.tipo === "like" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> ha dado like{" "}
                                        <Heart size={16} />
                                    </p>
                                )}

                                {n.tipo === "comentario" && (
                                    <p>
                                        <strong>{n.emisor_nombre}</strong> ha comentado{" "}
                                        <MessageCircle size={16} />
                                    </p>
                                )}

                                <span className="notificacion-date">
                                    {new Date(n.fecha_creacion).toLocaleString("es-ES")}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

export default NotificacionesPage