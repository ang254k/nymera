import { apiRequest } from "./client"

export async function getNotificaciones() {
    return apiRequest("/notificaciones")
}

export function marcarNotificacionLeida(id) {
    return apiRequest(`/notificaciones/${id}/leer`, {
        method: "PUT"
    })
}

export function marcarTodasComoLeidas() {
    return apiRequest("/notificaciones/marcar-todas", {
        method: "PATCH"
    })
}