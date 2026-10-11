# Funciones recursivas del prototipo Sumapaz.
# Cada una tiene su caso base explicito para evitar
# el desbordamiento de memoria (Stack Overflow).

from dominio.finca import Finca
from dominio.lote import Lote
from dominio.cultivo import Cultivo


def costo_acumulado_nodo(nodo):
    """
    Suma jerarquica: Finca -> Lote -> Cultivo -> Insumo.

    CASO BASE: nodo sin hijos -> devuelve su valor.
    """
    if not nodo.tiene_hijos():
        return getattr(nodo, "valor", 0)

    total = 0
    if isinstance(nodo, Finca):
        for lote in nodo.lotes:
            total += costo_acumulado_nodo(lote)
    elif isinstance(nodo, Lote):
        for cultivo in nodo.cultivos:
            total += costo_acumulado_nodo(cultivo)
    elif isinstance(nodo, Cultivo):
        for insumo in nodo.insumos:
            total += costo_acumulado_nodo(insumo)
    return total


def capital_restante(mes, capital, precio_venta, costo_insumos):
    """
    Simulacion financiera mes a mes.

    CASO BASE 1 (quiebra): capital <= 0 -> devuelve el mes.
    CASO BASE 2 (exito): mes == 24 -> devuelve 24.
    """
    if capital <= 0:
        return mes
    if mes == 24:
        return 24
    nuevo = capital + (precio_venta - costo_insumos)
    return capital_restante(mes + 1, nuevo, precio_venta, costo_insumos)


def indice_vulnerabilidad_sucesion(miembro):
    """
    Suma acumulativa de la cadena familiar.

    CASO BASE: miembro activo mas joven -> devuelve su indice.
    """
    if miembro.es_el_mas_joven():
        return miembro.indice
    if miembro.hijo is None:
        return miembro.indice
    return miembro.indice + indice_vulnerabilidad_sucesion(miembro.hijo)
