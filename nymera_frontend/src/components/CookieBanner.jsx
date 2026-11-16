import { useState, useEffect } from "react"
import { useTranslation } from "react-i18next"
import { Link } from "react-router-dom"

function CookieBanner() {
    const { t } = useTranslation()
    const [isVisible, setIsVisible] = useState(false)

    useEffect(() => {
        const cookiesAccepted = localStorage.getItem("cookiesAccepted")
        if (!cookiesAccepted) {
            setIsVisible(true)
        }
    }, [])

    const handleAccept = () => {
        localStorage.setItem("cookiesAccepted", "true")
        setIsVisible(false)
    }

    if (!isVisible) return null

    return (
        <div className="cookie-banner" role="region" aria-label={t("cookies.ariaLabel")}>
            <div className="cookie-content">
                <p className="cookie-text">
                    {t("cookies.message")}{" "}
                    <Link to="/privacy" className="cookie-link">
                        {t("cookies.privacyLink")}
                    </Link>.
                </p>
                <div className="cookie-actions">
                    <button
                        type="button"
                        className="btn btn-primary"
                        onClick={handleAccept}
                    >
                        {t("cookies.accept")}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default CookieBanner