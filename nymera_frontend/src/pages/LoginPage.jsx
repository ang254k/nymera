import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useNavigate } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { login, me } from "../api/auth"

import SEO from "../components/SEO"

import { getErrorMessage } from "../utils/getErrorMessage"
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

        if (!email.trim() || !password) {
            showToast(t("errors.fillAllFields"), "error")
            return
        }

        setLoading(true)

        try {
            await login({ email, password })

            const user = await me()

            loginUser(user)

            showToast(t("auth.loginSuccess"), "success")

            navigate("/home")

        } catch (err) {
            showToast(getErrorMessage(err, t), "error")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="page-center">
            <SEO
                title={t('seo.login.title')}
                description={t('seo.login.description')}
            />

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
                        noValidate
                    >
                        <label className="label stack-sm">
                            {t("auth.email")}

                            <input
                                className="input"
                                type="email"
                                placeholder={t("auth.emailPlaceholder")}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                autoComplete="email"
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
                                autoComplete="current-password"
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
                            aria-busy={loading}
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