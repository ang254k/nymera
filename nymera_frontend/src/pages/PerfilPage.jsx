import { useEffect, useState, useRef } from "react"

import {
    getSuenosByUser,
    getLikedSuenosByUser
} from "../api/suenos"
import { updateMe, uploadAvatar, changePassword } from "../api/usuarios"
import { me } from "../api/auth"

import SuenoCard from "../components/SuenoCard"
import Avatar from "../components/Avatar"

import { Heart } from "../lib/icons"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"
import { useDreamFilter } from "../context/DreamFilterContext"


function PerfilPage() {
    const { user, updateUserData } = useAuth()

    const [suenos, setSuenos] = useState([])
    const [suenosLikeados, setSuenosLikeados] = useState([])
    const [editando, setEditando] = useState(false)
    const [nuevoNombre, setNuevoNombre] = useState("")
    const [passwordActualPerfil, setPasswordActualPerfil] = useState("")
    const [passwordActualCambio, setPasswordActualCambio] = useState("")
    const [nuevaPassword, setNuevaPassword] = useState("")
    const [confirmarPassword, setConfirmarPassword] = useState("")
    const fileInputRef = useRef(null)

    const { categoriasSeleccionadas, orden } = useDreamFilter()
    const hayFiltros = categoriasSeleccionadas.length > 0 || orden.field !== null

    const { showToast } = useToast()

    const [loading, setLoading] = useState(true)
    const [loadingSuenos, setLoadingSuenos] = useState(true)
    const [error, setError] = useState("")
    const [savingPerfil, setSavingPerfil] = useState(false)
    const [changingPassword, setChangingPassword] = useState(false)

    useEffect(() => {
        async function load() {
            setLoadingSuenos(true)
            try {
                const data = await getSuenosByUser(user.id, categoriasSeleccionadas, orden.field, orden.direction)
                const likedData = await getLikedSuenosByUser(user.id, categoriasSeleccionadas, orden.field, orden.direction)

                setSuenos(data)
                setSuenosLikeados(likedData)

            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
                setLoadingSuenos(false)
            }
        }

        if (user) {
            load()
        }
    }, [user, categoriasSeleccionadas, orden.field, orden.direction])

    // Sincronizar input nombre con usuario autenticado
    useEffect(() => {
        if (user) {
            setNuevoNombre(user.nombre)
        }
    }, [user])


    function handleDelete(id) {
        setSuenos(prev => prev.filter(s => s.id !== id))
    }


    async function handleUpdatePerfil(e) {
        e.preventDefault()

        if(savingPerfil) return

        setSavingPerfil(true)

        try {
            await updateMe({
                nombre: nuevoNombre,
                current_password: passwordActualPerfil
            })

            const usuarioActualizado = await me()
            updateUserData(usuarioActualizado)

            showToast("Perfil actualizado", "success")

            setPasswordActualPerfil("")
            setEditando(false)
        }
        catch (err) {
            showToast(err.message, "error")
        } finally {
            setSavingPerfil(false)
        }
    }

    async function handleChangePassword(e) {
        e.preventDefault()

        if (changingPassword) return

        if (nuevaPassword !== confirmarPassword) {
            showToast("Las contraseñas no coinciden", "error")
            setConfirmarPassword("")
            return
        }

        setChangingPassword(true)

        try {
            await changePassword(passwordActualCambio, nuevaPassword)
            showToast("Contraseña actualizada", "success")

            setPasswordActualCambio("")
            setNuevaPassword("")
            setConfirmarPassword("")
        } catch (err) {
            showToast(err.message, "error")
        } finally {
            setChangingPassword(false)
        }

    }

    async function handleAvatarUpload(e) {
        const file = e.target.files[0]

        if (!file) return

        try {
            const usuarioActualizado = await uploadAvatar(file)

            updateUserData(usuarioActualizado)

            showToast("Avatar actualizado", "success")

            e.target.value = ""
        } catch (err) {
            showToast(err.message, "error")
        }
    }

    if (!user) {
        return (
            <p className="perfil-message">
                Debes iniciar sesión
            </p>
        )
    }

    if (loading) {
        return (
            <p className="perfil-loading">
                Cargando perfil...
            </p>
        )
    }
    if (error) {
        return (
            <p className="perfil-error">
                {error}
            </p>)
    }

    const suenosLikeadosExternos = suenosLikeados.filter(s => s.usuario_id !== user.id)

    return (

        <div className="perfil-page">
            <div className="perfil-card">

                {/* Avatar */}
                <Avatar
                    avatarUrl={user.avatar_url}
                    nombre={user.nombre}
                    size={80}
                    clickable={false}
                />

                <input
                    type="file"
                    accept="image/*"
                    ref={fileInputRef}
                    onChange={handleAvatarUpload}
                    className="perfil-avatar-input"
                />
                <button
                    className="perfil-avatar-button"
                    onClick={() => fileInputRef.current?.click()}
                >
                    Cambiar avatar
                </button>


                {/* Info */}
                <div className="perfil-info">

                    <h1 className="perfil-name">
                        {user.nombre}
                    </h1>

                    <p className="perfil-email">
                        {user.email}
                    </p>

                    <p className="perfil-member-since">
                        Miembro desde{" "}
                        {new Date(user.fecha_creacion).toLocaleDateString("es-ES")}
                    </p>

                    {/* Num sueños y likes */}
                    <div className="perfil-stats">
                        <span>
                            <strong>{suenos.length}</strong> sueños
                        </span>

                        <span className="perfil-stats-separator">·</span>

                        <span>
                            <strong>
                                {suenosLikeados.length}
                            </strong> likes
                        </span>
                    </div>


                    {/* Editar Perfil */}
                    <button
                        className="perfil-edit-button"
                        onClick={() => setEditando(!editando)}
                    >
                        Editar perfil
                    </button>


                    {editando && (
                        <form
                            className="perfil-edit-form"
                            onSubmit={handleUpdatePerfil}
                        >
                            <input
                                className="input"
                                type="text"
                                placeholder="Nuevo nombre"
                                value={nuevoNombre}
                                onChange={(e) => setNuevoNombre(e.target.value)}
                            />

                            <input
                                className="input"
                                type="password"
                                placeholder="Contraseña actual"
                                value={passwordActualPerfil}
                                onChange={(e) => setPasswordActualPerfil(e.target.value)}
                            />

                            <button
                                className="btn btn-primary"
                                type="submit"
                                disabled={savingPerfil}
                            >
                                {savingPerfil ? "Guardando..." : "Guardar cambios"}
                            </button>
                        </form>
                    )}

                    <hr className="perfil-divider" />

                    <h3 className="perfil-password-title">
                        Cambiar contraseña
                    </h3>

                    <form
                        className="perfil-password-form"
                        onSubmit={handleChangePassword}
                    >
                        <input
                            className="input"
                            type="password"
                            placeholder="Contraseña actual"
                            value={passwordActualCambio}
                            onChange={(e) => setPasswordActualCambio(e.target.value)}
                        />

                        <input
                            className="input"
                            type="password"
                            placeholder="Nueva contraseña"
                            value={nuevaPassword}
                            onChange={(e) => setNuevaPassword(e.target.value)}
                        />

                        <input
                            className="input"
                            type="password"
                            placeholder="Repetir nueva contraseña"
                            value={confirmarPassword}
                            onChange={(e) => setConfirmarPassword(e.target.value)}
                        />

                        <button
                            className="btn btn-primary"
                            type="submit"
                            disabled={changingPassword}
                        >
                            {changingPassword ? "Cambiando..." : "Cambiar contraseña"}
                        </button>
                    </form>

                </div>
            </div>

            {/* Sueños publicados */}
            <section className="perfil-dreams">

                <h2 className="perfil-section-title">
                    Sueños publicados
                </h2>

                {loadingSuenos ? (
                    <p className="perfil-loading">
                        Cargando sueños publicados...
                    </p>
                ) : suenos.length === 0 ? (
                    hayFiltros ? (
                        <p className="perfil-empty">No hay sueños que coincidan con los filtros seleccionados.</p>
                    ) : (
                        <p className="perfil-empty">No has publicado sueños aún</p>
                    )
                ) : (
                    suenos.map((sueno) => (
                        <SuenoCard
                            key={sueno.id}
                            sueno={sueno}
                            onSuenoEliminado={handleDelete}
                        />
                    ))
                )}
            </section>

            {/* Sueños Likeados */}
            <section className="perfil-liked">
                <h2 className="perfil-section-title">
                    <Heart size={20} />
                    <span>Sueños que te gustaron</span>
                </h2>

                {loadingSuenos ? (
                    <p className="perfil-loading">
                        Cargando sueños que te gustaron...
                    </p>
                ) : suenosLikeadosExternos.length === 0 ? (
                    hayFiltros ? (
                        <p className="perfil-empty">
                            No hay sueños que coincidan con los filtros seleccionados.
                        </p>
                    ) : (
                        <p className="perfil-empty">
                            Aún no has dado like a ningún sueño
                        </p>
                    )
                ) : (
                    <div className="perfil-liked-list">
                        {suenosLikeadosExternos.map((sueno) => (
                            <SuenoCard
                                key={sueno.id}
                                sueno={sueno}
                            />
                        ))}
                    </div>
                )}
            </section>

        </div>
    )
}

export default PerfilPage