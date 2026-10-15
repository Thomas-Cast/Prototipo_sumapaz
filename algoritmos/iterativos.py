# ============================================================
# Funciones con ciclos tradicionales.
# Se usan sobre listas planas (muestras, ofertas).
# ============================================================

def promedio_ph(muestras):
    """Promedio lineal con validacion interna (for tradicional)."""
    suma = 0
    validas = 0
    for m in muestras:
        if isinstance(m, (int, float)) and 0 < m < 14:
            suma += m
            validas += 1
    return suma / validas if validas > 0 else None


def almacen_mas_barato_por_producto(catalogo):
    """
    Recorre el diccionario producto -> [(almacen, precio), ...]
    y devuelve, por producto, el almacen mas barato y los empates.
    """
    resultado = {}
    for producto, ofertas in catalogo.items():
        mejor_almacen = None
        mejor_precio = float("inf")
        for almacen, precio in ofertas:
            if precio < mejor_precio:
                mejor_almacen, mejor_precio = almacen, precio
        empatados = [a for a, p in ofertas if p == mejor_precio]
        resultado[producto] = (mejor_almacen, mejor_precio, empatados)
    return resultado