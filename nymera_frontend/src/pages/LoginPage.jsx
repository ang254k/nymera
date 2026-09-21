import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { login, me } from "../api/auth"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"

function LoginPage() {

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const { loginUser } = useAuth()
    const { showToast } = useToast()

    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleLogin(e) {
        e.preventDefault()

        if (loading) return

        setLoading(true)

        try {
            const data = await login({ email, password })

            //Se guarda el token
            localStorage.setItem("token", data.access_token)

            //Ahora se puede llamar a me
            const user = await me()

            loginUser(data.access_token, user)

            showToast("Sesión iniciada", "success")

            navigate("/home")

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
                        Iniciar sesión
                    </h2>

                    <form
                        className="stack"
                        onSubmit={handleLogin}
                    >
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
                        </label>

                        <Link
                            className="forgot-link"
                            to="/forgot-password"
                        >
                            ¿Olvidaste tu contraseña?
                        </Link>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Iniciando sesión..." : "Iniciar sesión"}
                        </button>

                    </form>
                    <p className="auth-footer">
                        ¿No tienes cuenta todavía?
                    </p>
                    <Link
                        className="auth-link"
                        to="/register"
                    >
                        Crear una cuenta →
                    </Link>


                </div>
            </div>
        </div>
    )
}

export default LoginPage