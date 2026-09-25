import { useTranslation } from "react-i18next"
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
    const { t } = useTranslation()

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
                {t("filter.explore")}
            </h3>

            <hr className="divider" />

            <h4 className="dream-filter-section-title">
                <ChevronDown size={16} />
                {t("filter.categories")}
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
                {t("filter.sort")}
            </h4>

            <div className="dream-filter-order">
                <button
                    className="dream-filter-order-row"
                    onClick={() => cambiarOrden("fecha")}
                >
                    <span>
                        <CalendarDays size={16} />
                        {t("filter.date")}
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
                        {t("filter.likes")}
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
                        {t("filter.comments")}
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