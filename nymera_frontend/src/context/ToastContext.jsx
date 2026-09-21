import { CircleCheck, CircleAlert, Info, } from "../lib/icons"
import { createContext, useContext, useState } from "react"

const ToastContext = createContext()

export function ToastProvider({ children }) {
    const [toast, setToast] = useState(null)

    function showToast(message, type = "info") {
        setToast({ message, type })

        setTimeout(() => {
            setToast(null)
        }, 3000);
    }

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}

            {toast && (
                <div
                    className={`toast toast-${toast.type}`}
                    role="status"
                    aria-live="polite"
                >

                    {toast.type === "success" && (
                        <CircleCheck size={18} />
                    )}

                    {toast.type === "error" && (
                        <CircleAlert size={18} />
                    )}

                    {toast.type === "info" && (
                        <Info size={18} />
                    )}
                    <span>
                        {toast.message}
                    </span>

                </div>
            )}
        </ToastContext.Provider>
    )
}

export function useToast() {
    return useContext(ToastContext)
}