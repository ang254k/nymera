function ConfirmModal({
    open,
    title,
    message,
    confirmText = "Borrar",
    cancelText = "Cancelar",
    loading = false,
    onConfirm,
    onCancel
}) {
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
                onClick={(e) => e.stopPropagation()}
            >
                <h2
                    id="confirm-modal-title"
                    className="confirm-modal-title"
                >
                    {title}
                </h2>

                <p className="confirm-modal-message">
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
                        {loading ? "Eliminando..." : confirmText}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConfirmModal