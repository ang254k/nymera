import { useEffect, useState, useRef } from "react"
import { useTranslation } from "react-i18next"
import { useNavigate } from "react-router-dom"

import {
    getSuenosByUser,
    getLikedSuenosByUser
} from "../api/suenos"
import { updateMe, uploadAvatar, changePassword, deleteAccount } from "../api/usuarios"
import { me } from "../api/auth"

import SuenoCard from "../components/SuenoCard"
import Avatar from "../components/Avatar"
import SEO from "../components/SEO"
import ConfirmModal from "../components/ConfirmModal"

import { Heart } from "../lib/icons"

import { getErrorMessage } from "../utils/getErrorMessage"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"
import { useDreamFilter } from "../context/DreamFilterContext"


function PerfilPage() {
    const { t } = useTranslation()
    const navigate = useNavigate()

    const { user, updateUserData, logoutUser } = useAuth()

    const [suenos, setSuenos] = useState([])
    const [suenosLikeados, setSuenosLikeados] = useState([])
    const [editando, setEditando] = useState(false)
    const [nuevoNombre, setNuevoNombre] = useState("")
    const [passwordActualPerfil, setPasswordActualPerfil] = useState("")
    const [passwordActualCambio, setPasswordActualCambio] = useState("")
    const [nuevaPassword, setNuevaPassword] = useState("")
    const [confirmarPassword, setConfirmarPassword] = useState("")
    const fileInputRef = useRef(null)
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
    const [passwordEliminarCuenta, setPasswordEliminarCuenta] = useState("")
    const [deletingAccount, setDeletingAccount] = useState(false)

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
                setError(getErrorMessage(err, t))
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

        if (savingPerfil) return

        if (!nuevoNombre.trim() || !passwordActualPerfil) {
            showToast(t("profile.messages.fillAllFields"), "error")
            return
        }

        setSavingPerfil(true)

        try {
            await updateMe({
                nombre: nuevoNombre,
                current_password: passwordActualPerfil
            })

            const usuarioActualizado = await me()
            updateUserData(usuarioActualizado)

            showToast(t("profile.messages.profileUpdated"), "success")

            setPasswordActualPerfil("")
            setEditando(false)
        }
        catch (err) {
            showToast(getErrorMessage(err, t), "error")
        } finally {
            setSavingPerfil(false)
        }
    }

    async function handleChangePassword(e) {
        e.preventDefault()

        if (changingPassword) return

        if (!passwordActualCambio || !nuevaPassword || !confirmarPassword) {
            showToast(t("profile.messages.fillAllFields"), "error")
            return
        }

        if (nuevaPassword !== confirmarPassword) {
            showToast(t("profile.password.mismatch"), "error")
            setConfirmarPassword("")
            return
        }

        setChangingPassword(true)

        try {
            await changePassword(passwordActualCambio, nuevaPassword)
            showToast(t("profile.messages.passwordUpdated"), "success")

            setPasswordActualCambio("")
            setNuevaPassword("")
            setConfirmarPassword("")
        } catch (err) {
            showToast(getErrorMessage(err, t), "error")
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

            showToast(t("profile.messages.avatarUpdated"), "success")

            e.target.value = ""
        } catch (err) {
            showToast(getErrorMessage(err, t), "error")
        }
    }

    async function handleDeleteAccount() {
        if (deletingAccount) return

        if (!passwordEliminarCuenta) {
            showToast(t("profile.messages.fillAllFields"), "error")
            return
        }

        setDeletingAccount(true)

        try {
            await deleteAccount(passwordEliminarCuenta)

            setIsDeleteModalOpen(false)
            setPasswordEliminarCuenta("")
            showToast(t("profile.messages.accountDeleted"), "success")
            navigate("/login")
            await logoutUser()

        } catch (err) {
            showToast(getErrorMessage(err, t), "error")
        } finally {
            setDeletingAccount(false)
            setIsDeleteModalOpen(false)
            setPasswordEliminarCuenta("")
        }
    }

    const suenosLikeadosExternos = suenosLikeados.filter(s => s.usuario_id !== user.id)

    return (
        <div className="perfil-page">
            <SEO
                title={t('seo.perfil.title')}
                description={t('seo.perfil.description')}
            />

            {!user ? (
                <p className="perfil-message">
                    {t("profile.loginRequired")}
                </p>
            ) : loading ? (
                <p className="perfil-loading" role="status" aria-live="polite">
                    {t("profile.loading")}
                </p>
            ) : error ? (
                <p className="perfil-error" role="alert">
                    {error}
                </p>
            ) : (
                <>
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
                            aria-hidden="true"
                            tabIndex={-1}
                        />
                        <button
                            type="button"
                            className="perfil-avatar-button"
                            onClick={() => fileInputRef.current?.click()}
                            aria-label={t("accessibility.changeAvatar")}
                        >
                            {t("profile.avatar.change")}
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
                                {t("profile.info.memberSince")}{" "}
                                {new Date(user.fecha_creacion).toLocaleDateString("es-ES")}
                            </p>

                            {/* Num sueños y likes */}
                            <div className="perfil-stats">
                                <span>
                                    <strong>{suenos.length}</strong> {t("profile.info.dreams")}
                                </span>

                                <span className="perfil-stats-separator" aria-hidden="true">·</span>

                                <span>
                                    <strong>
                                        {suenosLikeados.length}
                                    </strong> {t("profile.info.likes")}
                                </span>
                            </div>


                            {/* Editar Perfil */}
                            <button
                                type="button"
                                className="perfil-edit-button"
                                onClick={() => setEditando(!editando)}
                                aria-expanded={editando}
                            >
                                {t("profile.edit.title")}
                            </button>


                            {editando && (
                                <form
                                    className="perfil-edit-form"
                                    onSubmit={handleUpdatePerfil}
                                    noValidate
                                >
                                    {/* Campo oculto de usuario para accesibilidad de Chrome */}
                                    <input
                                        type="text"
                                        autoComplete="username"
                                        value={user?.email || ""}
                                        style={{ display: "none" }}
                                        readOnly
                                    />

                                    <input
                                        className="input"
                                        type="text"
                                        placeholder={t("profile.edit.newName")}
                                        value={nuevoNombre}
                                        onChange={(e) => setNuevoNombre(e.target.value)}
                                        autoComplete="name"
                                    />

                                    <input
                                        className="input"
                                        type="password"
                                        placeholder={t("profile.edit.currentPassword")}
                                        value={passwordActualPerfil}
                                        onChange={(e) => setPasswordActualPerfil(e.target.value)}
                                        autoComplete="current-password"
                                    />

                                    <button
                                        className="btn btn-primary"
                                        type="submit"
                                        disabled={savingPerfil}
                                        aria-busy={savingPerfil}
                                    >
                                        {savingPerfil ? t("profile.edit.saving") : t("profile.edit.save")}
                                    </button>
                                </form>
                            )}

                            <hr className="perfil-divider" />

                            <h3 className="perfil-password-title">
                                {t("profile.password.title")}
                            </h3>

                            <form
                                className="perfil-password-form"
                                onSubmit={handleChangePassword}
                                noValidate
                            >
                                {/* Campo oculto de usuario para accesibilidad de Chrome */}
                                <input
                                    type="text"
                                    autoComplete="username"
                                    value={user?.email || ""}
                                    style={{ display: "none" }}
                                    readOnly
                                />

                                <input
                                    className="input"
                                    type="password"
                                    placeholder={t("profile.password.current")}
                                    value={passwordActualCambio}
                                    onChange={(e) => setPasswordActualCambio(e.target.value)}
                                    autoComplete="current-password"
                                />

                                <input
                                    className="input"
                                    type="password"
                                    placeholder={t("profile.password.new")}
                                    value={nuevaPassword}
                                    onChange={(e) => setNuevaPassword(e.target.value)}
                                    autoComplete="new-password"
                                />

                                <input
                                    className="input"
                                    type="password"
                                    placeholder={t("profile.password.repeat")}
                                    value={confirmarPassword}
                                    onChange={(e) => setConfirmarPassword(e.target.value)}
                                    autoComplete="new-password"
                                />

                                <button
                                    className="btn btn-primary"
                                    type="submit"
                                    disabled={changingPassword}
                                    aria-busy={changingPassword}
                                >
                                    {changingPassword ? t("profile.password.changing") : t("profile.password.change")}
                                </button>
                            </form>

                            <div className="perfil-danger-zone">
                                <button
                                    type="button"
                                    className="btn btn-danger btn-full"
                                    onClick={() => setIsDeleteModalOpen(true)}                                >
                                    {t("profile.deleteAccount.button")}
                                </button>
                            </div>

                        </div>
                    </div>

                    {/* Sueños publicados */}
                    <section className="perfil-dreams">

                        <h2 className="perfil-section-title">
                            {t("profile.dreams.title")}
                        </h2>

                        {loadingSuenos ? (
                            <p className="perfil-loading" role="status" aria-live="polite">
                                {t("profile.dreams.loading")}
                            </p>
                        ) : suenos.length === 0 ? (
                            hayFiltros ? (
                                <p className="perfil-empty">{t("profile.dreams.emptyWithFilters")}</p>
                            ) : (
                                <p className="perfil-empty">{t("profile.dreams.empty")}</p>
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
                            <Heart size={20} aria-hidden="true" />
                            <span>{t("profile.likedDreams.title")}</span>
                        </h2>

                        {loadingSuenos ? (
                            <p className="perfil-loading" role="status" aria-live="polite">
                                {t("profile.likedDreams.loading")}
                            </p>
                        ) : suenosLikeadosExternos.length === 0 ? (
                            hayFiltros ? (
                                <p className="perfil-empty">
                                    {t("profile.likedDreams.emptyWithFilters")}
                                </p>
                            ) : (
                                <p className="perfil-empty">
                                    {t("profile.likedDreams.empty")}
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
                </>
            )}
            <ConfirmModal
                open={isDeleteModalOpen}
                title={t("profile.deleteAccount.modalTitle")}
                message={t("profile.deleteAccount.modalDesc")}
                confirmText={t("profile.deleteAccount.confirm")}
                cancelText={t("dreamCard.cancel")}
                loadingText={t("profile.deleteAccount.deleting")}
                loading={deletingAccount}
                onConfirm={handleDeleteAccount}
                onCancel={() => {
                    setIsDeleteModalOpen(false)
                    setPasswordEliminarCuenta("")
                }}
            >
                <form
                    onSubmit={(e) => { e.preventDefault(); handleDeleteAccount(); }}
                    className="modal-input-container"
                >
                    <label className="label" style={{ marginBottom: "8px" }}>
                        {t("profile.deleteAccount.placeholder")}
                    </label>

                    {/* Campo oculto opcional para silenciar Chrome en modales */}
                    <input
                        type="text"
                        autoComplete="username"
                        value={user?.email || ""}
                        style={{ display: "none" }}
                        readOnly
                    />

                    <input
                        className="input"
                        type="password"
                        placeholder={t("profile.deleteAccount.placeholder")}
                        value={passwordEliminarCuenta}
                        onChange={(e) => setPasswordEliminarCuenta(e.target.value)}
                        autoComplete="new-password"
                    />
                </form>
            </ConfirmModal>
        </div>
    )
}

export default PerfilPage