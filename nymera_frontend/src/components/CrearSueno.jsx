import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { createSueno } from "../api/suenos"
import { getCategorias } from "../api/categorias"
import { getErrorMessage } from "../utils/getErrorMessage"
import { useToast } from "../context/ToastContext"

function CrearSueno({ onSuenoCreado }) {
    const { t } = useTranslation()

    const [titulo, setTitulo] = useState("")
    const [categorias, setCategorias] = useState([])
    const [categoriaId, setCategoriaId] = useState("")
    const [contenido, setContenido] = useState("")
    const [publico, setPublico] = useState(true)
    const [saving, setSaving] = useState(false)

    const [error, setError] = useState("")
    const { showToast } = useToast()

    useEffect(() => {
        async function loadCategorias() {
            try {
                const data = await getCategorias()
                setCategorias(data)

            } catch (err) {
                showToast(t("dream.loadCategoriesError"), "error")
            }
        }
        loadCategorias()
    }, [])

    async function handleSubmit(e) {
        e.preventDefault()
        if (saving) return

        setError("")
        setSaving(true)

        try {
            const nuevoSueno = await createSueno({
                titulo,
                contenido,
                categoria_id: categoriaId,
                publico
            })

            onSuenoCreado(nuevoSueno)
            showToast(t("dream.published"), "success")
            setTitulo("")
            setContenido("")
            setCategoriaId("")
            setPublico(true)

        } catch (err) {
            setError(getErrorMessage(err, t))
        } finally {
            setSaving(false)
        }
    }

    return (
        <div className="card crear-sueno">
            <h3 className="crear-sueno-title">
                {t("dream.createTitle")}
            </h3>
            {error && (
                <p className="form-error">
                    {error}
                </p>
            )}


            <form className="form" onSubmit={handleSubmit}>
                <input
                    className="input"
                    type="text"
                    placeholder={t("dream.titlePlaceholder")}
                    value={titulo}
                    onChange={(e) => setTitulo(e.target.value)}
                />

                <select
                    className="select"
                    value={categoriaId}
                    onChange={(e) => {
                        const value = e.target.value
                        setCategoriaId(value === "" ? "" : Number(value))
                    }}
                >
                    <option value="">{t("dream.selectCategory")}</option>
                    {categorias.map(c => (
                        <option key={c.id} value={c.id}>
                            {c.nombre}
                        </option>
                    ))}
                </select>

                <textarea
                    className="textarea"
                    placeholder={t("dream.contentPlaceholder")}
                    value={contenido}
                    onChange={(e) => setContenido(e.target.value)}
                />

                <label className="crear-sueno-public">
                    <input
                        type="checkbox"
                        checked={publico}
                        onChange={(e) => setPublico(e.target.checked)}
                    />
                    {t("dream.makePublic")}
                </label>

                <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={saving}>
                    {saving ? t("dream.publishing") : t("dream.publish")}
                </button>
            </form>
        </div>
    )

}

export default CrearSueno