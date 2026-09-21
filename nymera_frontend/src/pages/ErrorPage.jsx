import { useNavigate } from "react-router-dom"
import error404Image from "../assets/404-dream.png"

function ErrorPage() {
    const navigate = useNavigate()

    return (
        <main className="page-center error-page">
            <div className="container-sm error-content">

                <img
                    src={error404Image}
                    alt={"Sueño perdido"}
                    className="error-illustration"
                />

                <h1 className="error-title">
                    Página no encontrada
                </h1>

                <p className="error-description">
                    Parece que este sueño se ha desvanecido...
                    <br />
                    Pero no te preocupes, siempre hay más por descubrir.
                </p>

                <button
                    className="btn btn-primary"
                    onClick={() => navigate("/home")}
                >
                    Volver al inicio
                </button>

            </div>
        </main>
    )
}

export default ErrorPage