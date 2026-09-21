import { apiRequest } from "./client";

export function getSuenosByHashtag(
    nombre, 
    categorias = [], 
    ordenarPor = null, 
    direccion = null
) {
    const params = new URLSearchParams()

    categorias.forEach((id) => {
        params.append("categorias", id)
    })

    if (ordenarPor) {
        params.append("ordenar_por", ordenarPor)
    }
    if (direccion) {
        params.append("direccion", direccion)
    }


    return apiRequest(`/hashtags/${encodeURIComponent(nombre)}?${params.toString()}`)
}

export function getTrendingHashtags() {
    return apiRequest(`/hashtags/trending`)
}