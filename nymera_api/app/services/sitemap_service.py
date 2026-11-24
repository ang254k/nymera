from datetime import datetime, timezone
from urllib.parse import quote
from xml.sax.saxutils import escape

from app.config import settings
from app.repositories.sitemap_repository import SitemapRepository


class SitemapService:

    def __init__(self, sitemap_repository: SitemapRepository | None = None):
        self.sitemap_repository = sitemap_repository or SitemapRepository()

    def _get_api_base_url(self) -> str:
        backend_url = getattr(settings, "BACKEND_URL", None)
        if backend_url:
            return backend_url.rstrip("/")
        return "https://nymera-backend.onrender.com"

    def _get_frontend_base_url(self) -> str:
        return settings.FRONTEND_URL.rstrip("/")

    def _format_lastmod(self, fecha_creacion: datetime | None) -> str | None:
        if fecha_creacion is None:
            return None
        if isinstance(fecha_creacion, str):
            return fecha_creacion[:10]
        if fecha_creacion.tzinfo is None:
            fecha_creacion = fecha_creacion.replace(tzinfo=timezone.utc)
        return fecha_creacion.astimezone(timezone.utc).strftime("%Y-%m-%d")

    def _render_urlset(self, urls: list[tuple[str, str | None]]) -> str:
        url_blocks: list[str] = []
        for loc, lastmod in urls:
            lines = [
                "  <url>",
                f"    <loc>{escape(loc)}</loc>",
            ]
            if lastmod:
                lines.append(f"    <lastmod>{escape(lastmod)}</lastmod>")
            lines.append("  </url>")
            url_blocks.append("\n".join(lines))

        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(url_blocks)
            + "\n</urlset>\n"
        )

    def build_sitemap_index_xml(self) -> str:
        api_base = self._get_api_base_url()
        sitemap_locs = [
            f"{api_base}/sitemap-pages.xml",
            f"{api_base}/sitemap-suenos.xml",
            f"{api_base}/sitemap-hashtags.xml",
        ]

        sitemap_blocks = [
            f"  <sitemap>\n    <loc>{escape(loc)}</loc>\n  </sitemap>"
            for loc in sitemap_locs
        ]

        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(sitemap_blocks)
            + "\n</sitemapindex>\n"
        )

    def build_pages_sitemap_xml(self) -> str:
        frontend_base = self._get_frontend_base_url()
        urls: list[tuple[str, str | None]] = [
            (f"{frontend_base}/home", None),
            (f"{frontend_base}/privacy", None),
            (f"{frontend_base}/terms", None),
        ]
        return self._render_urlset(urls)

    def build_suenos_sitemap_xml(self) -> str:
        frontend_base = self._get_frontend_base_url()
        suenos = self.sitemap_repository.get_public_suenos()
        urls: list[tuple[str, str | None]] = []

        for sueno_id, fecha_creacion in suenos:
            loc = f"{frontend_base}/suenos/{sueno_id}"
            lastmod = self._format_lastmod(fecha_creacion)
            urls.append((loc, lastmod))

        return self._render_urlset(urls)

    def build_hashtags_sitemap_xml(self) -> str:
        frontend_base = self._get_frontend_base_url()
        hashtags = self.sitemap_repository.get_public_hashtags()
        urls: list[tuple[str, str | None]] = []

        for raw_name in hashtags:
            clean_name = (raw_name or "").lstrip("#").strip()
            if clean_name:
                encoded_name = quote(clean_name, safe="")
                urls.append((f"{frontend_base}/hashtags/{encoded_name}", None))

        return self._render_urlset(urls)