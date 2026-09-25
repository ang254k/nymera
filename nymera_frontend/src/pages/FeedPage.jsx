import { useEffect, useRef, useState } from "react"
import { useTranslation } from "react-i18next"

import { getFeed } from "../api/suenos"

import SuenoCard from "../components/SuenoCard"
import CrearSueno from "../components/CrearSueno"

import { useAuth } from "../context/AuthContext"
import { useToast } from "../context/ToastContext"
import { useDreamFilter } from "../context/DreamFilterContext"

function FeedPage() {
    const { t } = useTranslation()

    const [suenos, setSuenos] = useState([])
    const [loading, setLoading] = useState(true)
    const [loadingMore, setLoadingMore] = useState(false)
    const [page, setPage] = useState(1)
    const [hasMore, setHasMore] = useState(true)

    const sentinelRef = useRef(null)

    const { showToast } = useToast()
    const { user } = useAuth()
    const { categoriasSeleccionadas, orden } = useDreamFilter()

    useEffect(() => {
        async function loadFeed() {

            setLoading(true)
            setPage(1)
            setHasMore(true)

            try {
                const data = await getFeed(1, categoriasSeleccionadas, orden.field, orden.direction)

                setSuenos(data)
                setHasMore(data.length === 20)
            } catch (err) {
                showToast(t("feed.loadError"), "error")
            } finally {
                setLoading(false)
            }
        }

        loadFeed()
    }, [categoriasSeleccionadas, orden.field, orden.direction])

    async function loadMore() {
        if (loadingMore || !hasMore) return

        setLoadingMore(true)

        const nextPage = page + 1

        try {
            const data = await getFeed(
                nextPage,
                categoriasSeleccionadas,
                orden.field,
                orden.direction
            )
            setSuenos((prev) => [...prev, ...data])
            setPage(nextPage)
            setHasMore(data.length === 20)
        } catch (err) {
            showToast(t("feed.loadMoreError"), "error")
        } finally {
            setLoadingMore(false)
        }
    }

    useEffect(() => {
        if (loading || !hasMore) return

        const sentinel = sentinelRef.current
        if (!sentinel) return

        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    loadMore()
                }
            },
            {
                rootMargin: "300px"
            }
        )
        observer.observe(sentinel)

        return () => {
            observer.disconnect()
        }
    }, [loading, hasMore, loadingMore, page, categoriasSeleccionadas, orden.field, orden.direction])


    function handleNuevoSueno(sueno) {
        setSuenos((prev) => [sueno, ...prev])
    }

    function handleDelete(id) {
        setSuenos((prev) => prev.filter((s) => s.id !== id))
    }

    if (loading) return (
        <p className="feed-loading">
            {t("feed.loading")}
        </p>
    )


    return (
        <div className="feed-page">

            {/* Componente CrearSueno (Solo si se está logueado)*/}
            {user && (
                <div className="feed-create">
                    <CrearSueno onSuenoCreado={handleNuevoSueno} />
                </div>
            )}

            {suenos.length === 0 ? (
                <p className="feed-empty">
                    {t("feed.empty")}
                </p>
            ) : (
                <>
                    <div className="feed-list">
                        {suenos.map((sueno) => (
                            <SuenoCard
                                key={sueno.id}
                                sueno={sueno}
                                onSuenoEliminado={handleDelete}
                            />
                        ))}
                    </div>

                    {hasMore && (
                        <div ref={sentinelRef} className="feed-sentinel" />
                    )}

                    {loadingMore && (
                        <p className="feed-loading-more">
                            {t("feed.loadingMore")}
                        </p>
                    )}
                </>

            )}

        </div>
    )

}

export default FeedPage