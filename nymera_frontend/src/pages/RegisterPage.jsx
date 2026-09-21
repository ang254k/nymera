import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { register } from "../api/auth"
import { useToast } from "../context/ToastContext"

function RegisterPage() {
    const [nombre, setNombre] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const [loading, setLoading] = useState(false)

    const { showToast } = useToast()
    const navigate = useNavigate()

    async function handleRegister(e) {
        e.preventDefault()

        if (password !== confirmPassword) {
            showToast("Las contraseñas no coinciden", "error")
            setConfirmPassword("")
            return
        }

        if (loading) return

        setLoading(true)

        try {
            await register({ nombre, email, password })

            showToast("Usuario creado correctamente", "success")

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
                        Crear una cuenta
                    </h2>

                    <form
                        className="stack"
                        onSubmit={handleRegister}
                    >

                        <label className="label stack-sm">

                            Nombre

                            <input
                                className="input"
                                type="text"
                                placeholder="Tu nombre"
                                value={nombre}
                                onChange={(e) => setNombre(e.target.value)}
                            />

                        </label>

                        <label className="label stack-sm">

                            Correo electrónico

                            <input
                                className="input"
                                type="email"
                                placeholder="correo@ejemplo.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />

                        </label>

                        <label className="label stack-sm">

                            Contraseña

                            <input
                                className="input"
                                type="password"
                                placeholder="Introduce tu contraseña"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <p className="form-help">
                                Mínimo 8 caracteres.
                            </p>
                        </label>

                        <label className="label stack-sm">

                            Confirmar contraseña

                            <input
                                className="input"
                                type="password"
                                placeholder="Confirma tu contraseña"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Creando cuenta..." : "Crear cuenta"}
                        </button>

                    </form>

                    <p className="auth-footer">
                        ¿Ya tienes una cuenta?
                    </p>

                    <Link
                        className="auth-link"
                        to="/login"
                    >
                        Iniciar sesión
                    </Link>

                </div>

            </div>

        </div>

    )
}

export default RegisterPage