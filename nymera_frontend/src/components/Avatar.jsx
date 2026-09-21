import { useNavigate } from "react-router-dom"

import { API_URL } from "../config/api"

function Avatar({
    avatarUrl,
    nombre,
    usuarioId,
    size = 40,
    clickable = true
}) {
    const navigate = useNavigate()

    function handleClick(e) {
        if (!clickable || !usuarioId) return

        e.stopPropagation()
        
        navigate(`/usuarios/${usuarioId}`)
    }

    return (
        <div
            className={`avatar ${clickable ? "avatar-clickable" : ""}`}
            onClick={handleClick}
            style={{
                width: size,
                height: size,
            }}
        >
            {avatarUrl ? (
                <img
                    src={`${API_URL}${avatarUrl}`}
                    alt={nombre}
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