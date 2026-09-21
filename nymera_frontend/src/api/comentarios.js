import { apiRequest } from "./client"

export function getComentarios(suenoId) {
    return apiRequest(`/suenos/${suenoId}/comentarios`)
}

export function createComentario(suenoId, contenido) {
    return apiRequest(`/suenos/${suenoId}/comentarios`, {
        method: "POST",
        body: JSON.stringify({ contenido })
    })
}

export async function deleteComentario(comentarioId) {
    return apiRequest(`/comentarios/${comentarioId}`,
        {
            method: "DELETE"
        }
    )
}

export async function updateComentario(comentarioId, contenido) {
    return apiRequest(`/comentarios/${comentarioId}`, {
        method: "PUT",
        body: JSON.stringify({
            contenido
        })
    })
}