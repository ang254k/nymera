import { useEffect } from "react"

function ConfirmModal({
    open,
    title,
    message,
    confirmText,
    cancelText,
    loadingText,
    loading = false,
    onConfirm,
    onCancel
}) {
    // Para cerrar con la tecla Esc
    useEffect(() => {
        function handleKeyDown(e) {
            if (e.key === "Escape" && open && !loading) {
                onCancel()
            }
        }
        window.addEventListener("keydown", handleKeyDown)
        return () => window.removeEventListener("keydown", handleKeyDown)
    }, [open, loading, onCancel])

    if (!open) return null

    return (
        <div
            className="confirm-modal-backdrop"
            onClick={onCancel}
        >
            <div
                className="confirm-modal"
                role="dialog"
                aria-modal="true"
                aria-labelledby="confirm-modal-title"
                aria-describedby="confirm-modal-desc"
                onClick={(e) => e.stopPropagation()}
            >
                <h2
                    id="confirm-modal-title"
                    className="confirm-modal-title"
                >
                    {title}
                </h2>

                <p
                    id="confirm-modal-desc"
                    className="confirm-modal-message"
                >

                    {message}
                </p>

                <div className="confirm-modal-actions">
                    <button
                        className="btn btn-secondary"
                        onClick={onCancel}
                        disabled={loading}
                    >
                        {cancelText}
                    </button>

                    <button
                        className="btn btn-danger"
                        onClick={onConfirm}
                        disabled={loading}
                    >
                        {loading ? loadingText : confirmText}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmModal