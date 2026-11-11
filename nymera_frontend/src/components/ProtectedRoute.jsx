import { useEffect, useRef } from "react"
import { useTranslation } from "react-i18next"
import { Navigate, useLocation } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"


function ProtectedRoute({ children }) {
    const { t } = useTranslation()
    const { user, loading } = useAuth()
    const { showToast } = useToast()
    const location = useLocation()
    const hasWarned = useRef(false)

    useEffect(() => {
        if (!loading && !user && !hasWarned.current && location.pathname !== "/" && location.pathname !== "/home") {
            showToast(t("auth.loginRequired"), "error")
            hasWarned.current = true
        }
    }, [loading, user, showToast, location.pathname])

    if (loading) {
        return <p>{t("auth.loading")}</p>
    }

    if (!user) {
        return <Navigate to="/login" replace/>
    }

    return children
}

export default ProtectedRoute