import { createContext, useContext, useEffect, useState } from "react";
import { me } from "../api/auth"

const AuthContext = createContext()

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadUser() {
            const token = localStorage.getItem("token")

            if (!token) {
                setLoading(false)
                return
            }

            try {
                const data = await me()
                setUser(data)
            } catch {
                localStorage.removeItem("token")
                setUser(null)
            } finally {
                setLoading(false)
            }
        }

        loadUser()
    }, [])

    function loginUser(token, userData) {
        localStorage.setItem("token", token)
        setUser(userData)
    }

    function updateUserData(newData) {
        setUser(prev => ({
            ...prev,
            ...newData
        }))
    }

    function logoutUser() {
        localStorage.removeItem("token")
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, loginUser, logoutUser, updateUserData }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    return useContext(AuthContext)
}
