import { Helmet } from 'react-helmet-async'
import { useTranslation } from 'react-i18next'
import { APP_NAME, APP_TAGLINE } from '../config/app'

export default function SEO({ title, description }) {
    const { i18n } = useTranslation()
    const siteTitle = title ? `${title} — ${APP_NAME}` : `${APP_NAME} — ${APP_TAGLINE}`

    return (
        <Helmet htmlAttributes={{ lang: i18n.language }}>
            <title>{siteTitle}</title>
            {description && <meta name="description" content={description} />}
        </Helmet>
    )
}