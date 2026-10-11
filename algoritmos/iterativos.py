# Funciones con ciclos tradicionales (for).
# Se usan para listas planas, no para jerarquias.
# Incluyen validacion interna que descarta datos erroneos
# sin romper el ciclo.


def promedio_ph(muestras):
    """
    Calcula el promedio de las muestras de pH de un lote.

    Recorre la lista con un for. Si encuentra un valor que no
    es numero o esta fuera del rango 0-14, lo descarta y sigue.
    Devuelve None si no hay muestras validas.
    """
    suma = 0
    validas = 0
    for m in muestras:
        if isinstance(m, (int, float)) and 0 < m < 14:
            suma += m
            validas += 1
        else:
            print(f"Muestra descartada: {m}")
    return suma / validas if validas > 0 else None


def almacen_mas_barato(precios):
    """
    Encuentra el almacen con el precio mas bajo para un insumo.

    Recorre la lista de pares (nombre, precio) con un for.
    Descarta precios negativos o no numericos.
    Devuelve (None, None) si no hay precios validos.
    """
    if not precios:
        return None, None
    mejor_nombre, mejor_precio = None, float("inf")
    for nombre, precio in precios:
        if isinstance(precio, (int, float)) and 0 < precio < mejor_precio:
            mejor_nombre, mejor_precio = nombre, precio
    return mejor_nombre, mejor_precio
