import { useNavigate } from "react-router-dom"
import { useTranslation } from "react-i18next"

import SEO from "../components/SEO"

import error404Image from "../assets/404-dream.png"

function ErrorPage() {
    const { t } = useTranslation()
    const navigate = useNavigate()

    return (
        <main className="page-center error-page">
            <SEO
                title={t('seo.error.title')}
                description={t('seo.error.description')}
            />
            
            <div className="container-sm error-content">

                <img
                    src={error404Image}
                    alt={t("error.alt")}
                    className="error-illustration"
                />

                <h1 className="error-title">
                    {t("error.title")}
                </h1>

                <p className="error-description">
                    {t("error.description")}
                    <br />
                    {t("error.descriptionContinue")}
                </p>

                <button
                    className="btn btn-primary"
                    onClick={() => navigate("/home")}
                >
                    {t("error.backHome")}
                </button>

            </div>
        </main>
    )
}

export default ErrorPage