import { useEffect } from "react"
import { useTranslation } from "react-i18next"
import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"


function ProtectedRoute({ children }) {
    const { t } = useTranslation()
    const { user, loading } = useAuth()
    const { showToast } = useToast()

    useEffect(() => {
        if (!loading && !user) {
            showToast(t("auth.loginRequired"), "error")
        }
    }, [loading, user, showToast])

    if (loading) {
        return <p>{t("auth.loading")}</p>
    }

    if (!user) {
        return <Navigate to="/login" replace/>
    }

    return children
}

export default ProtectedRoute