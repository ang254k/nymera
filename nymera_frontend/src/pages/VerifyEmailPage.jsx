import { useEffect, useRef, useState } from "react"
import { useTranslation } from "react-i18next"
import { Link, useParams } from "react-router-dom"

import { APP_NAME, APP_LOGO } from "../config/app"
import { verifyEmail } from "../api/auth"
import SEO from "../components/SEO"
import { getErrorMessage } from "../utils/getErrorMessage"

export default function VerifyEmailPage() {
    const { t } = useTranslation()
    const { token } = useParams()

    const [status, setStatus] = useState("verifying")
    const hasRequestedRef = useRef(false)
    const [error, setError] = useState(null)

    useEffect(() => {
        if (!token || hasRequestedRef.current) return
        hasRequestedRef.current = true

        async function runVerification() {
            try {
                await verifyEmail(token)
                setStatus("success")
            } catch (err) {
                setStatus("error")
                setError(err)
            }
        }

        runVerification()
    }, [token])

    const displayMessage =
        status === "verifying"
            ? t("auth.verifyingEmail")
            : status === "success"
                ? t("success.email_verified")
                : getErrorMessage(error, t)

    return (
        <div className="page-center">
            <SEO
                title={t("seo.verifyEmail.title")}
                description={t("seo.verifyEmail.description")}
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
                            {t("auth.tagline")}
                        </p>
                    </div>

                    <div className={`verify-status-icon verify-status-icon--${status}`} aria-hidden="true">
                        {status === "verifying" && (
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M21 12a9 9 0 1 1-6.219-8.56" strokeLinecap="round" />
                            </svg>
                        )}
                        {status === "success" && (
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                                <circle cx="12" cy="12" r="9" />
                                <path d="m9 12 2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                        )}
                        {status === "error" && (
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                                <circle cx="12" cy="12" r="9" />
                                <path d="M12 8v4m0 4h.01" strokeLinecap="round" />
                            </svg>
                        )}
                    </div>

                    <h2 className="section-title">
                        {t("auth.verifyEmailTitle")}
                    </h2>

                    <p className="auth-description" aria-live="polite">
                        {displayMessage}
                    </p>

                    {status !== "verifying" && (
                        <Link
                            className="btn btn-primary btn-full"
                            to="/login"
                        >
                            {t("auth.goToLogin")}
                        </Link>
                    )}
                </div>
            </div>
        </div>
    )
}