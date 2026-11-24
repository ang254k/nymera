from fastapi import APIRouter, Response

from app.services.sitemap_service import SitemapService

router = APIRouter(tags=["Sitemap"])
sitemap_service = SitemapService()

XML_MEDIA_TYPE = "application/xml; charset=utf-8"


@router.get("/sitemap.xml")
def get_sitemap_index():
    xml_content = sitemap_service.build_sitemap_index_xml()
    return Response(content=xml_content, media_type=XML_MEDIA_TYPE)


@router.get("/sitemap-pages.xml")
def get_pages_sitemap():
    xml_content = sitemap_service.build_pages_sitemap_xml()
    return Response(content=xml_content, media_type=XML_MEDIA_TYPE)


@router.get("/sitemap-suenos.xml")
def get_suenos_sitemap():
    xml_content = sitemap_service.build_suenos_sitemap_xml()
    return Response(content=xml_content, media_type=XML_MEDIA_TYPE)


@router.get("/sitemap-hashtags.xml")
def get_hashtags_sitemap():
    xml_content = sitemap_service.build_hashtags_sitemap_xml()
    return Response(content=xml_content, media_type=XML_MEDIA_TYPE)
