import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"

import { getSuenosByHashtag } from "../api/hashtag"
import SuenoCard from "../components/SuenoCard"
import { useToast } from "../context/ToastContext"
import { useDreamFilter } from "../context/DreamFilterContext"

export default function HashtagPage() {

    const { nombre } = useParams()
    const { showToast } = useToast()
    const [suenos, setSuenos] = useState([])
    const [loadingInicial, setLoadingInicial] = useState(true)
    const [loadingSuenos, setLoadingSuenos] = useState(true)
    const { categoriasSeleccionadas, orden } = useDreamFilter()
    const hayFiltros = categoriasSeleccionadas.length > 0 || orden.field !== null


    useEffect(() => {
        async function loadHashtag() {
            try {
                setLoadingSuenos(true)

                const data = await getSuenosByHashtag(nombre, categoriasSeleccionadas, orden.field, orden.direction)

                setSuenos(data)
            } catch (err) {
                showToast(err.message || "Error cargando hashtag", "error")
            } finally {
                setLoadingInicial(false)
                setLoadingSuenos(false)
            }
        }
        loadHashtag()
    }, [nombre, categoriasSeleccionadas, orden.field, orden.direction])

    if (loadingInicial) {
        return <p className="hashtag-loading">Cargando...</p>
    }

    return (
        <div className="hashtag-page">
            <h2 className="hashtag-title">
                #{nombre}
            </h2>

            {loadingSuenos ? (
                <p className="hashtag-loading">
                    Cargando sueños...
                </p>
            ) :
                suenos.length === 0 ? (
                    hayFiltros ? (
                        <p className="hashtag-empty">No hay sueños con este hashtag que coincidan con los filtros seleccionados</p>
                    ) : (
                        <p className="hashtag-empty">No hay sueños con este hashtag.</p>
                    )
                ) : (
                    <div className="hashtag-dreams">
                        {suenos.map((sueno) => (
                            <SuenoCard
                                key={sueno.id}
                                sueno={sueno}
                            />
                        ))}
                    </div>
                )}
        </div>
    )
}  