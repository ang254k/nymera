import { useState } from "react"
import { Link } from "react-router-dom"
import { APP_NAME, APP_TAGLINE, APP_LOGO } from "../config/app"

import { forgotPassword } from "../api/auth"

import { useToast } from "../context/ToastContext"

export default function ForgotPasswordPage() {

    const { showToast } = useToast()

    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e) {
        e.preventDefault()

        if (loading) return

        setLoading(true)
        
        try {
            setLoading(true)

            const data = await forgotPassword(email)

            showToast(data.message, "success")

            setEmail("")
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
                        Recuperar contraseña
                    </h2>

                    <p className="auth-description">
                        Introduce tu correo electrónico. Si existe una cuenta asociada,
                        recibirás un enlace para restablecer la contraseña.
                    </p>

                    <form className="stack" onSubmit={handleSubmit}>

                        <label className="label stack-sm">

                            Correo electrónico

                            <input
                                className="input"
                                type="email"
                                placeholder="Introduce tu correo electrónico"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />

                        </label>

                        <button
                            className="btn btn-primary btn-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Enviando..." : "Enviar enlace"}
                        </button>

                    </form>

                    <p className="auth-footer">
                        ¿Recordaste tu contraseña?
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