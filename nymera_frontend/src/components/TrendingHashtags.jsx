import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getTrendingHashtags } from "../api/hashtag"

function TrendingHashtags() {
    const { t } = useTranslation()

    const [hashtags, setHashtags] = useState([])

    const navigate = useNavigate()

    useEffect(() => {
        async function loadTrending() {
            try {
                const data = await getTrendingHashtags()
                setHashtags(data)
            } catch (err) {
                setHashtags([])
            }
        }
        loadTrending()
    }, [])

    if (hashtags.length === 0) {
        return null
    }

    return (
        <div className="card trending-hashtags">
            <h3 className="trending-hashtags-title">
                {t("trending.title")}
            </h3>

            <div className="trending-hashtag-list">
                {hashtags.map((hashtag) => (
                    <button
                        className="trending-hashtag"
                        key={hashtag}
                        onClick={() => navigate(`/hashtags/${hashtag}`)}
                    >
                        #{hashtag}
                    </button>
                ))}
            </div>

        </div>
    )
}

export default TrendingHashtags