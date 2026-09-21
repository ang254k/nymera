import { Link } from "react-router-dom";

export default function HashtagText({ texto }) {
    const partes = texto.split(/(#[\p{L}\p{N}_]+)/gu)

    return partes.map((parte, index) => {

        if (parte.startsWith("#")) {

            const hashtag = parte.slice(1)

            return (
                <Link
                    key={index}
                    to={`/hashtags/${hashtag}`}
                    onClick={(e) => e.stopPropagation()}
                    className="hashtag-link"
                >
                    {parte}
                </Link>
            )
        }

        return parte
    })
}