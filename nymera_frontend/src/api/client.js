import { API_URL } from "../config/api"


export async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("token")

    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    }

    if (token) {
        headers["Authorization"] = `Bearer ${token}`
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    })

    let data = null

    try {
        data = await response.json()
    } catch {

    }

    if (!response.ok) {
        let message = "request_error"

        if (data?.detail) {
            if (typeof data.detail === "string") {
                message = data.detail
            } else if (Array.isArray(data.detail)) {
                message = "validation_error"
            }
        }

        throw new Error(message)
    }

    return data
}