import { apiRequest } from "./client"

export async function getNotificaciones() {
    return apiRequest("/notificaciones/")
}

export function marcarNotificacionLeida(id) {
    return apiRequest(`/notificaciones/${id}/leer`, {
        method: "PUT"
    })
}