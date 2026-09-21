import { Outlet } from "react-router-dom"

import PageTransition from "./PageTransition"
import Header from "./Header"
import Footer from "./Footer"

function LayoutPublico() {
    return (
        <div className="layout-publico">
            <Header />

            <main className="layout-publico-content">
                <PageTransition>
                    <Outlet />
                </PageTransition>
            </main>

            <Footer />
        </div>
    )
}

export default LayoutPublico