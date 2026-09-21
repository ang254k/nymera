import { apiRequest } from "./client"

export function getCategorias() {
    return apiRequest("/categorias")
}