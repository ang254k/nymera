import { apiRequest } from "./client"

export function register({ nombre, email, password }) {
    return apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify({ nombre, email, password }),
    })
}

export function login({ email, password }) {
    return apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
    })
}

export function me() {
    return apiRequest("/auth/me", {
        method: "GET",
    })
}

export function forgotPassword(email) {
    return apiRequest("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email })
    })
}

export function resetPassword(token, newPassword) {
    return apiRequest("/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({
            token,
            new_password: newPassword,
        }),
    })
}