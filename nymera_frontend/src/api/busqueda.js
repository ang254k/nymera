import { apiRequest } from "./client"

export async function search(
    q,
    categorias = [],
    ordenarPor = null,
    direccion = null
) {
    const params = new URLSearchParams()

    params.append("q", q)

    categorias.forEach((id) => {
        params.append("categorias", id)
    })

    if (ordenarPor) {
        params.append("ordenar_por", ordenarPor)
    }

    if (direccion) {
        params.append("direccion", direccion)
    }
    
    return apiRequest(
        `/search?${params.toString()}`
    )
}