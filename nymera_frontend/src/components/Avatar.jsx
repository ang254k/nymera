import { useNavigate } from "react-router-dom"
import { useTranslation } from "react-i18next"
import { API_URL } from "../config/api"

function Avatar({
    avatarUrl,
    nombre,
    usuarioId,
    size = 40,
    clickable = true
}) {
    const { t } = useTranslation()
    const navigate = useNavigate()

    function handleClick(e) {
        if (!clickable || !usuarioId) return

        e.stopPropagation()

        navigate(`/usuarios/${usuarioId}`)
    }

    const getAvatarSrc = (url) => {
        if (!url) return null
        if (url.startsWith("http://") || url.startsWith("https://")) {
            return url
        }
        return `${API_URL}${url}`
    }
    return (
        <div
            className={`avatar ${clickable ? "avatar-clickable" : ""}`}
            onClick={handleClick}
            role={clickable && usuarioId ? "button" : undefined}
            tabIndex={clickable && usuarioId ? 0 : undefined}
            aria-label={clickable && usuarioId ? t("userProfile.viewProfile", { name: nombre || t("userProfile.defaultUser") }) : undefined}
            style={{
                width: size,
                height: size,
            }}
        >
            {avatarUrl ? (
                <img
                    src={getAvatarSrc(avatarUrl)}
                    alt={nombre ? t("profile.avatar.alt", { name: nombre }) : t("profile.avatar.defaultAlt")}
                    className="avatar-image"
                />
            ) : (
                <span className="avatar-initial">
                    {nombre?.[0]?.toUpperCase()}
                </span>
            )}
        </div>
    )


}

export default Avatar