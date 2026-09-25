import { useSearchParams, Link } from "react-router-dom"
import { useEffect, useState } from "react"
import { useTranslation } from "react-i18next"

import { search } from "../api/busqueda"

import SuenoCard from "../components/SuenoCard"
import Avatar from "../components/Avatar"

import { useDreamFilter } from "../context/DreamFilterContext"
import { useToast } from "../context/ToastContext"


export default function BusquedaPage() {
    const { t } = useTranslation()

    const [usuarios, setUsuarios] = useState([])
    const [suenos, setSuenos] = useState([])
    const [loadingResultados, setLoadingResultados] = useState(true)

    const { showToast } = useToast()
    const [searchParams] = useSearchParams()

    const { categoriasSeleccionadas, orden } = useDreamFilter()

    const q = searchParams.get("q")

    const hayFiltros = categoriasSeleccionadas.length > 0 || orden.field !== null

    useEffect(() => {
        async function loadResults() {
            try {
                setLoadingResultados(true)

                const data = await search(q, categoriasSeleccionadas, orden.field, orden.direction)

                setUsuarios(data.usuarios)
                setSuenos(data.suenos)

            } catch (err) {
                showToast(t("searchResults.error"), "error")
            } finally {
                setLoadingResultados(false)
            }
        }

        if (q) {
            loadResults()
        }
    }, [q, categoriasSeleccionadas, orden.field, orden.direction])

    if (loadingResultados) {
        return (
            <p className="search-loading">
                {t("searchResults.searching")}
            </p>
        )
    }

    return (

        <div className="search-page">
            <h2 className="search-title">
                {t("searchResults.title")} {q}
            </h2>

            {usuarios.length > 0 && (
                <section className="search-section">
                    <h3 className="search-section-title">
                        {t("searchResults.users")}
                    </h3>
                    <div className="search-users">
                        {usuarios.map((u) => (
                            <Link
                                key={u.id}
                                to={`/usuarios/${u.id}`}
                                className="search-user"
                            >
                                <Avatar
                                    avatarUrl={u.avatar_url}
                                    nombre={u.nombre}
                                    usuarioId={u.id}
                                    size={40}
                                    clickable={false}
                                />

                                <strong>{u.nombre}</strong>
                            </Link>
                        ))}
                    </div>
                </section>
            )}

            {suenos.length > 0 && (
                <section className="search-section">
                    <h3 className="search-section-title">
                        {t("searchResults.dreams")}
                    </h3>

                    <div className="search-dreams">
                        {suenos.map((sueno) => (
                            <SuenoCard
                                key={sueno.id}
                                sueno={sueno}
                                onSuenoEliminado={() => { }}
                            />
                        ))}
                    </div>
                </section>
            )}

            {usuarios.length === 0 &&
                suenos.length === 0 && (
                    <p className="search-empty">
                        {hayFiltros
                            ? t("searchResults.emptyWithFilters")
                            : t("searchResults.empty")
                        }
                    </p>
                )}
        </div>
    )
}