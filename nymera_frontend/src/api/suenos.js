import { apiRequest } from "./client"

export function getFeed(
    page = 1,
    categorias = [],
    ordenarPor = null,
    direccion = null
) {
    const params = new URLSearchParams()

    params.append("page", page)

    categorias.forEach((id) => {
        params.append("categorias", id)
    })

    if (ordenarPor) {
        params.append("ordenar_por", ordenarPor)
    }
    if (direccion) {
        params.append("direccion", direccion)
    }
    return apiRequest(`/home?${params.toString()}`)
}

export function getSuenoDetalle(id) {
    return apiRequest(`/suenos/${id}`)
}

export function toggleLike(id) {
    return apiRequest(`/suenos/${id}/like`, {
        method: "POST"
    })
}

export function createSueno({ titulo, contenido, categoria_id, publico }) {
    return apiRequest("/suenos", {
        method: "POST",
        body: JSON.stringify({
            titulo,
            contenido,
            categoria_id,
            publico
        })
    })
}

export function deleteSueno(id) {
    return apiRequest(`/suenos/${id}`, {
        method: "DELETE"
    })
}

export function updateSueno(id, data) {
    return apiRequest(`/suenos/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
    })
}

// perfil
export function getSuenosByUser(
    userId,
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

    return apiRequest(`/usuarios/${userId}/suenos?${params.toString()}`)
}

export async function getLikedSuenosByUser(
    userId,
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

    return apiRequest(`/suenos/usuarios/${userId}/likes?${params.toString()}`)
}