import { useState } from "react"
import { useTranslation } from "react-i18next"
import { useNavigate } from "react-router-dom"

function SearchBar() {
    const { t } = useTranslation()

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
            placeholder={t("search.placeholder")}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
        />
    )
}

export default SearchBar