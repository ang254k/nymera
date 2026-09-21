class FiltroRepository:
    
    def construir_filtros_y_orden(
        self,
        categorias=None,
        ordenar_por=None,
        direccion=None,
        orden_defecto="ORDER BY s.fecha_creacion DESC",
    ):
        where_extra = ""
        parametros = []

        if categorias:
            where_extra += """
            AND s.categoria_id = ANY(%s)
            """
            parametros.append(categorias)

        campos = {
            "fecha": "s.fecha_creacion",
            "likes": "likes_count",
            "comentarios": "comentarios_count",
        }

        order_by = orden_defecto

        if ordenar_por in campos:
            campo = campos[ordenar_por]

            if direccion == "asc":
                order_by = f"ORDER BY {campo} ASC"
            elif direccion == "desc":
                order_by = f"ORDER BY {campo} DESC"

        return where_extra, parametros, order_by
