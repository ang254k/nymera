import { useEffect } from "react"
import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"


function ProtectedRoute({ children }) {
    const { user, loading } = useAuth()
    const { showToast } = useToast()

    useEffect(() => {
        if (!loading && !user) {
            showToast("Debes iniciar sesión", "error")
        }
    }, [loading, user, showToast])

    if (loading) {
        return <p>Cargando...</p>
    }

    if (!user) {
        return <Navigate to="/login" replace/>
    }

    return children
}

export default ProtectedRoute