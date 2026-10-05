import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Link } from "react-router-dom"
import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { forgotPassword } from "../api/auth"

import { getErrorMessage } from "../utils/getErrorMessage"
import { useToast } from "../context/ToastContext"

export default function ForgotPasswordPage() {
    const { t } = useTranslation()

    const { showToast } = useToast()

    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()

        if (loading) return

        setLoading(true)

        try {
            await forgotPassword(email)

            showToast(t("success.password_reset_email_sent"), "success")

            setEmail("")
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
                        {t("auth.forgotPasswordTitle")}
                    </h2>

                    <p className="auth-description">
                        {t("auth.forgotPasswordDescription")}
                    </p>

                    <form className="stack" onSubmit={handleSubmit}>

                        <label className="label stack-sm">

                            {t("auth.email")}

                            <input
                                className="input"
                                type="email"
                                placeholder={t("auth.emailPlaceholderForgot")}
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? t("auth.sending") : t("auth.sendLink")}
                        </button>

                    </form>

                    <p className="auth-footer">
                        {t("auth.rememberedPassword")}
                    </p>

                    <Link
                        className="auth-link"
                        to="/login"
                    >
                        {t("auth.backToLogin")}
                    </Link>


                </div>

            </div>
        </div>
    )

}