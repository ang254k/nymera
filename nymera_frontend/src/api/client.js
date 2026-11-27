import { API_URL } from "../config/api"

export async function apiRequest(endpoint, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
        credentials: "include"
    })

    if (response.status === 204) {
        return null
    }

    const contentType = response.headers.get("content-type") || ""
    const isJson = contentType.includes("application/json")

    let data = null

    if (isJson) {
        try {
            data = await response.json()
        } catch {
            if (response.ok) {
                throw new Error("invalid_json_response")
            }
        }
    } else if (response.ok) {
        throw new Error("unexpected_response_format")
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