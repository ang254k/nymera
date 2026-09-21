import { useEffect, useState } from "react"
import { createSueno } from "../api/suenos"
import { getCategorias } from "../api/categorias"
import { useToast } from "../context/ToastContext"

function CrearSueno({ onSuenoCreado }) {

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
                showToast("Error cargando categorías", "error")
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
            showToast("Sueño publicado", "success")
            setTitulo("")
            setContenido("")
            setCategoriaId("")
            setPublico(true)

        } catch (err) {
            setError(err.message)
        } finally {
            setSaving(false)
        }
    }

    return (
        <div className="card crear-sueno">
            <h3 className="crear-sueno-title">
                ¿Qué has soñado?
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
                    placeholder="Título"
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
                    <option value="">Selecciona categoría</option>
                    {categorias.map(c => (
                        <option key={c.id} value={c.id}>
                            {c.nombre}
                        </option>
                    ))}
                </select>

                <textarea
                    className="textarea"
                    placeholder="Cuenta tu sueño..."
                    value={contenido}
                    onChange={(e) => setContenido(e.target.value)}
                />

                <label className="crear-sueno-public">
                    <input
                        type="checkbox"
                        checked={publico}
                        onChange={(e) => setPublico(e.target.checked)}
                    />
                    Hacer público
                </label>

                <button
                    className="btn btn-primary"
                    type="submit"
                    disabled={saving}>
                    {saving ? "Publicando..." : "Publicar"}
                </button>
            </form>
        </div>
    )

}

export default CrearSueno