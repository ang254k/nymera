import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useNavigate, useParams } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { resetPassword } from "../api/auth"

import { getErrorMessage } from "../utils/getErrorMessage"

import { useToast } from "../context/ToastContext"

export default function ResetPasswordPage() {
    const { t } = useTranslation()

    const { token } = useParams()
    const navigate = useNavigate()
    const { showToast } = useToast()

    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()

        if (newPassword !== confirmPassword) {
            showToast(t("auth.passwordMismatch"), "error")
            return
        }

        if (loading) return

        setLoading(true)

        try {
            await resetPassword(token, newPassword)

            showToast(t("auth.resetPasswordSuccess"), "success")

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
                        {t("auth.resetPasswordTitle")}
                    </h2>

                    <p className="auth-description">
                        {t("auth.resetPasswordDescription")}
                    </p>

                    <form
                        className="stack"
                        onSubmit={handleSubmit}
                    >
                        <div className="stack-sm">

                            <label className="label stack-sm">

                                {t("auth.newPassword")}

                                <input
                                    className="input"
                                    type="password"
                                    placeholder={t("auth.newPasswordPlaceholder")}
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                />
                            </label>

                            <p className="form-help">
                                {t("auth.passwordHelp")}
                            </p>
                        </div>


                        <label className="label stack-sm">

                            {t("auth.confirmPassword")}

                            <input
                                className="input"
                                type="password"
                                placeholder={t("auth.confirmNewPasswordPlaceholder")}
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? t("auth.changingPassword") : t("auth.changePassword")}
                        </button>

                    </form>

                    <p className="auth-footer">
                        {t("auth.ready")}
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