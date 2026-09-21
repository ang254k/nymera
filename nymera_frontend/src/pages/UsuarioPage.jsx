import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import { getUsuario } from "../api/usuarios"
import { getSuenosByUser } from "../api/suenos"
import SuenoCard from "../components/SuenoCard"
import { useToast } from "../context/ToastContext"
import { useDreamFilter } from "../context/DreamFilterContext"
import Avatar from "../components/Avatar"


function UsuarioPage() {
    const { id } = useParams()

    const [suenos, setSuenos] = useState([])
    const [usuario, setUsuario] = useState(null)
    const [loading, setLoading] = useState(true)
    const [loadingSuenos, setLoadingSuenos] = useState(true)

    const { showToast } = useToast()
    const { categoriasSeleccionadas, orden } = useDreamFilter()
    const hayFiltros = categoriasSeleccionadas.length > 0 || orden.field !== null

    async function loadUsuario() {
        try {
            const usuarioData = await getUsuario(id)
            setUsuario(usuarioData)
        } catch (err) {
            showToast("Error cargando perfil", "error")
        } finally {
            setLoading(false)
        }
    }

    async function loadSuenos() {
        setLoadingSuenos(true)
        try {
            const suenoData = await getSuenosByUser(id, categoriasSeleccionadas, orden.field, orden.direction)
            setSuenos(suenoData)
        } catch (err) {
            showToast("Error cargando sueños", "error")
        } finally {
            setLoadingSuenos(false)
        }
    }

    useEffect(() => {
        loadUsuario()
    }, [id])

    useEffect(() => {
        loadSuenos()
    }, [
        id,
        categoriasSeleccionadas,
        orden.field,
        orden.direction
    ])

    if (loading || !usuario) {
        return <p className="usuario-page-loading">
            Cargando perfil...
        </p>
    }

    return (
        <div className="usuario-page">
            <div className="usuario-profile-card">
                {/* Avatar */}
                <Avatar
                    avatarUrl={usuario.avatar_url}
                    nombre={usuario.nombre}
                    usuarioId={usuario.id}
                />

                <h1 className="usuario-profile-name">
                    {usuario.nombre}
                </h1>

                <div className="usuario-profile-stats">
                    <span>
                        <strong>{suenos.length}</strong> sueños
                    </span>

                    <span>.</span>

                    <span>
                        <strong>
                            {suenos.reduce((acc, s) => acc + s.likes_count, 0)}
                        </strong> likes
                    </span>
                </div>

            </div>


            {/* Lista Sueños */}

            <h2 className="usuarios-suenos-title">
                Sueños públicos
            </h2>

            {loadingSuenos ? (

                <p className="usuario-suenos-loading">
                    Cargando sueños...
                </p>

            ) : suenos.length === 0 ? (
                hayFiltros ? (
                    <p className="usuarios-suenos-empty">No hay sueños que coincidan con los filtros seleccionados.</p>
                ) : (
                    <p className="usuarios-suenos-empty">Este usuario no tiene sueños públicos</p>
                )
            ) : (
                <div className="usuarios-suenos-list">
                    {suenos.map((sueno) => (
                        <SuenoCard
                            key={sueno.id}
                            sueno={sueno}
                        />
                    ))}
                </div>
            )}
        </div>
    )


}

export default UsuarioPage