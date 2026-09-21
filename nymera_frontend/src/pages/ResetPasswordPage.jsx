import { useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { resetPassword } from "../api/auth"

import { useToast } from "../context/ToastContext"

export default function ResetPasswordPage() {

    const { token } = useParams()
    const navigate = useNavigate()
    const { showToast } = useToast()

    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()

        if (newPassword !== confirmPassword) {
            showToast("Las contraseñas no coinciden", "error")
            return
        }

        if (loading) return

        setLoading(true)

        try {
            await resetPassword(token, newPassword)

            showToast("Contraseña actualizada correctamente", "success")

            navigate("/login")
        } catch (err) {
            showToast(err.message, "error")
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
                        Restablecer contraseña
                    </h2>

                    <p className="auth-description">
                        Introduce tu nueva contraseña para acceder de nuevo a tu cuenta.
                    </p>

                    <form
                        className="stack"
                        onSubmit={handleSubmit}
                    >
                        <div className="stack-sm">

                            <label className="label stack-sm">

                                Nueva contraseña

                                <input
                                    className="input"
                                    type="password"
                                    placeholder="Introduce tu nueva contraseña"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                />
                            </label>

                            <p className="form-help">
                                Mínimo 8 caracteres.
                            </p>
                        </div>


                        <label className="label stack-sm">

                            Confirmar contraseña

                            <input
                                className="input"
                                type="password"
                                placeholder="Confirma tu nueva contraseña"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Cambiando..." : "Cambiar contraseña"}
                        </button>

                    </form>

                    <p className="auth-footer">
                        ¿Todo listo?
                    </p>

                    <Link
                        className="auth-link"
                        to="/login"
                    >
                        Volver al inicio de sesión
                    </Link>


                </div>

            </div>
        </div>
    )

}