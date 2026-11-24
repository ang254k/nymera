from app.db import get_connection

class SitemapRepository:

    def get_public_suenos(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, fecha_creacion
                    FROM sueno
                    WHERE publico IS TRUE
                    ORDER BY fecha_creacion DESC NULLS LAST, id DESC
                    """
                )
                rows = cur.fetchall()
                return [(row[0], row[1]) for row in rows]

    def get_public_hashtags(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT h.nombre
                    FROM hashtag h
                    INNER JOIN sueno_hashtag sh ON sh.hashtag_id = h.id
                    INNER JOIN sueno s ON s.id = sh.sueno_id
                    WHERE s.publico IS TRUE
                      AND h.nombre IS NOT NULL
                      AND btrim(h.nombre) <> ''
                    ORDER BY h.nombre ASC
                    """
                )
                rows = cur.fetchall()
                return [row[0] for row in rows]