import { useDreamFilter } from "../context/DreamFilterContext"
import {
    CalendarDays,
    Heart,
    MessageCircle,
    ChevronDown,
    ArrowDown,
    ArrowUp
} from "../lib/icons"

function DreamFilter() {

    const {
        categorias,
        loadingCategorias,
        categoriasSeleccionadas,
        setCategoriasSeleccionadas,
        orden,
        setOrden
    } = useDreamFilter()


    function cambiarOrden(campo) {
        if (orden.field !== campo) {
            setOrden({
                field: campo,
                direction: "desc"
            })

            return
        }
        if (orden.direction === "desc") {
            setOrden({
                field: campo,
                direction: "asc"
            })
            return
        }

        setOrden({
            field: null,
            direction: null
        })
    }

    function getOrdenIcon(campo) {
        if (orden.field !== campo)
            return "-"
        if (orden.direction === "desc")
            return <ArrowDown size={16} />

        return <ArrowUp size={16} />
    }

    return (
        <div className="card dream-filter">
            <h3 className="dream-filter-title">
                Explorar
            </h3>

            <hr className="divider" />

            <h4 className="dream-filter-section-title">
                <ChevronDown size={16} />
                Categorías
            </h4>

            <div className="dream-filter-categories">
                {categorias.map((cat) => {
                    const seleccionada = categoriasSeleccionadas.includes(cat.id)

                    return (
                        <button
                            key={cat.id}
                            className={`dream-filter-chip ${seleccionada ? "is-selected" : ""
                                }`}
                            onClick={() => {
                                if (seleccionada) {
                                    setCategoriasSeleccionadas(
                                        categoriasSeleccionadas.filter(
                                            id => id !== cat.id
                                        )
                                    )
                                } else {
                                    setCategoriasSeleccionadas([
                                        ...categoriasSeleccionadas,
                                        cat.id
                                    ])
                                }
                            }}
                        >
                            {cat.nombre}
                        </button>
                    )
                })}
            </div>

            <hr className="divider" />

            <h4 className="dream-filter-section-title">
                <ChevronDown size={16} />
                Ordenar
            </h4>

            <div className="dream-filter-order">
                <button
                    className="dream-filter-order-row"
                    onClick={() => cambiarOrden("fecha")}
                >
                    <span>
                        <CalendarDays size={16} />
                        Fecha
                    </span>

                    <span>
                        {getOrdenIcon("fecha")}
                    </span>
                </button>

                <button
                    className="dream-filter-order-row"
                    onClick={() => cambiarOrden("likes")}

                >
                    <span>
                        <Heart size={16} />
                        Likes
                    </span>

                    <span>
                        {getOrdenIcon("likes")}
                    </span>
                </button>

                <button
                    className="dream-filter-order-row"
                    onClick={() => cambiarOrden("comentarios")}
                >
                    <span>
                        <MessageCircle size={16} />
                        Comentarios
                    </span>
                    <span>
                        {getOrdenIcon("comentarios")}
                    </span>
                </button>
            </div>

        </div>
    )
}

export default DreamFilter