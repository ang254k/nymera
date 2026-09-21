import { Outlet, useLocation } from "react-router-dom"

import Header from "./Header"
import Footer from "./Footer"
import SearchBar from "./SearchBar"
import TrendingHashtags from "./TrendingHashtags"
import DreamFilter from "./DreamFilter"
import PageTransition from "./PageTransition"

function LayoutPrivado() {
    const location = useLocation()

    const rutasConFiltro = [
        "/home",
        "/perfil",
        "/usuarios",
        "/hashtags",
        "/search"
    ]

    const mostrarDreamFilter = rutasConFiltro.some(ruta => location.pathname.startsWith(ruta))

    return (
        <>
            <Header />

            <div
                className={`layout-privado-search ${mostrarDreamFilter
                        ? "has-filter"
                        : "no-filter"
                    }`}
            >
                <SearchBar />
            </div>

            <div className="layout-privado-main">

                {/* Sidebar Izquierdo */}
                {mostrarDreamFilter && (
                    <aside className="layout-privado-filter">
                        <DreamFilter />
                    </aside>
                )}

                {/* Contenido principal */}
                <main className="layout-privado-content">
                    <PageTransition>
                        <Outlet />
                    </PageTransition>

                </main>

                {/* Sidebar derecho */}
                <aside className="layout-privado-trending">
                    <TrendingHashtags />
                </aside>
            </div>


            <Footer />

        </>
    )
}

export default LayoutPrivado