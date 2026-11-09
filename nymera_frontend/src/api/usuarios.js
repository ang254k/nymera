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

    const response = await fetch(
        `${API_URL}/usuarios/me/avatar`,
        {
            method: "POST",
            credentials: "include",
            body: formData
        }
    )
    let data = null
    try{
        data = await response.json()
    } catch {

    }

    if (!response.ok) {
        throw new Error(data?.detail || "avatar_upload_error")
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
