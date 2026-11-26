import { apiRequest } from "./client"

export function register({ nombre, email, password, turnstile_token, lang = "es" }) {
    return apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify({ nombre, email, password, turnstile_token, lang }),
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

export function logout() {
    return apiRequest("/auth/logout", {
        method: "POST",
    })
}

export function forgotPassword(email, lang = "es") {
    return apiRequest("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email, lang })
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

export function verifyEmail(token) {
    return apiRequest("/auth/verify-email", {
        method: "POST",
        body: JSON.stringify({ token }),
    })
}

export function resendVerification(email, lang = "es") {
    return apiRequest("/auth/resend-verification", {
        method: "POST",
        body: JSON.stringify({ email, lang }),
    })
}