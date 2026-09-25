import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useNavigate } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { login, me } from "../api/auth"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"

function LoginPage() {
    const { t } = useTranslation()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const { loginUser } = useAuth()
    const { showToast } = useToast()

    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleLogin(e) {
        e.preventDefault()

        if (loading) return

        setLoading(true)

        try {
            const data = await login({ email, password })

            //Se guarda el token
            localStorage.setItem("token", data.access_token)

            //Ahora se puede llamar a me
            const user = await me()

            loginUser(data.access_token, user)

            showToast(t("auth.loginSuccess"), "success")

            navigate("/home")

        } catch (err) {
            showToast(err.message, "error")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="page-center">
            <div className="container-sm">
                <div className="card auth-card">

                    <div className="brand">
                        <img
                            src={APP_LOGO}
                            alt={APP_NAME}
                            className="brand-logo"
                        />

                        <p className="auth-subtitle">
                            {APP_TAGLINE}
                        </p>
                    </div>

                    <h2 className="section-title">
                        {t("auth.loginTitle")}
                    </h2>

                    <form
                        className="stack"
                        onSubmit={handleLogin}
                    >
                        <label className="label stack-sm">
                            {t("auth.email")}

                            <input
                                className="input"
                                type="email"
                                placeholder={t("auth.emailPlaceholder")}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </label>


                        <label className="label stack-sm">
                            {t("auth.password")}
                            <input
                                className="input"
                                type="password"
                                placeholder={t("auth.passwordPlaceholder")}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </label>

                        <Link
                            className="forgot-link"
                            to="/forgot-password"
                        >
                            {t("auth.forgotPassword")}
                        </Link>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? t("auth.loggingIn") : t("auth.loginButton")}
                        </button>

                    </form>
                    <p className="auth-footer">
                        {t("auth.noAccount")}
                    </p>
                    <Link
                        className="auth-link"
                        to="/register"
                    >
                        {t("auth.createAccount")}
                    </Link>


                </div>
            </div>
        </div>
    )
}

export default LoginPage