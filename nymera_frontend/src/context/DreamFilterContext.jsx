import { createContext, useContext, useState, useEffect } from "react"
import { getCategorias } from "../api/categorias"

const DreamFilterContext = createContext()

export function DreamFilterProvider({ children }) {
    const [categorias, setCategorias] = useState([])
    const [loadingCategorias, setLoadingCategorias] = useState(true)

    const [categoriasSeleccionadas, setCategoriasSeleccionadas] = useState([])

    const [orden, setOrden] = useState({
        field: null,
        direction: null
    })

    useEffect(() => {
        async function loadCategorias() {
            try {
                const data = await getCategorias()
                setCategorias(data)
            } catch(err) {
                setCategorias([])
            }   finally {
                setLoadingCategorias(false)
            }
        }
        loadCategorias()
    }, [])

    return (
        <DreamFilterContext.Provider
            value={{
                categorias,
                loadingCategorias,
                setCategorias,

                categoriasSeleccionadas,
                setCategoriasSeleccionadas,

                orden,
                setOrden
            }}
        >
            {children}
        </DreamFilterContext.Provider>
    )

}

export function useDreamFilter() {
    return useContext(DreamFilterContext)
}