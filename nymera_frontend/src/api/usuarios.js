import { apiRequest } from "./client"
import { API_URL } from "../config/api"


export function updateMe(data) {
    return apiRequest("/usuarios/me", {
        method: "PUT",
        body: JSON.stringify(data),
    })
}

export async function uploadAvatar(file) {
    const formData = new FormData()

    formData.append("avatar", file)

    const token = localStorage.getItem("token")

    const response = await fetch(
        `${API_URL}/usuarios/me/avatar`,
        {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            },
            body: formData
        }
    )

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.detail || "Error al subir el avatar")
    }

    return data

}

export async function changePassword(currentPassword, newPassword) {
    return apiRequest("/usuarios/me/password", {
        method: "PUT",
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
        }),
    })
}

export function getUsuario(id) {
    return apiRequest(`/usuarios/${id}`)
}
