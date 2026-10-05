import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useNavigate } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { register } from "../api/auth"

import { getErrorMessage } from "../utils/getErrorMessage"
import { useToast } from "../context/ToastContext"

function RegisterPage() {
    const { t } = useTranslation()

    const [nombre, setNombre] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const [loading, setLoading] = useState(false)

    const { showToast } = useToast()
    const navigate = useNavigate()

    async function handleRegister(e) {
        e.preventDefault()

        if (password !== confirmPassword) {
            showToast(t("auth.passwordMismatch"), "error")
            setConfirmPassword("")
            return
        }

        if (loading) return

        setLoading(true)

        try {
            await register({ nombre, email, password })

            showToast(t("auth.registerSuccess"), "success")

            navigate("/login")

        } catch (err) {
            showToast(getErrorMessage(err, t), "error")
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
                        {t("auth.registerTitle")}
                    </h2>

                    <form
                        className="stack"
                        onSubmit={handleRegister}
                    >

                        <label className="label stack-sm">

                            {t("auth.name")}

                            <input
                                className="input"
                                type="text"
                                placeholder={t("auth.namePlaceholder")}
                                value={nombre}
                                onChange={(e) => setNombre(e.target.value)}
                            />

                        </label>

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
                            <p className="form-help">
                                {t("auth.passwordHelp")}
                            </p>
                        </label>

                        <label className="label stack-sm">

                            {t("auth.confirmPassword")}

                            <input
                                className="input"
                                type="password"
                                placeholder={t("auth.confirmPasswordPlaceholder")}
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? t("auth.registering") : t("auth.registerButton")}
                        </button>

                    </form>

                    <p className="auth-footer">
                        {t("auth.alreadyAccount")}
                    </p>

                    <Link
                        className="auth-link"
                        to="/login"
                    >
                        {t("auth.goToLogin")}
                    </Link>

                </div>

            </div>

        </div>

    )
}

export default RegisterPage