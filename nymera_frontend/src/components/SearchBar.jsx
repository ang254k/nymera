import { useState } from "react"
import { useNavigate } from "react-router-dom"

function SearchBar() {

    const [query, setQuery] = useState("")

    const navigate = useNavigate()

    function handleKeyDown(e) {

        if (e.key === "Enter" && query.trim()) {

            navigate(
                `/search?q=${encodeURIComponent(query)}`
            )
        }
    }

    return (
        <input
            className="input search-bar"
            type="text"
            placeholder="Buscar sueños, usuarios o hashtags..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
        />
    )
}

export default SearchBar