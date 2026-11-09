import { createContext, useContext, useEffect, useState } from "react";
import { me, logout as apiLogout } from "../api/auth"

const AuthContext = createContext()

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function loadUser() {
            try {
                const data = await me()
                setUser(data)
            } catch {
                setUser(null)
            } finally {
                setLoading(false)
            }
        }

        loadUser()
    }, [])

    function loginUser(userData) {
        setUser(userData)
    }

    function updateUserData(newData) {
        setUser(prev => ({
            ...prev,
            ...newData
        }))
    }

    async function logoutUser() {
        try {
            await apiLogout()
        } catch (error) {

        } finally {
            setUser(null)
        }
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
