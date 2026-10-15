# ============================================================
# Funciones recursivas del prototipo.
# Cada una tiene su caso base documentado para evitar
# desbordamiento de memoria.
# ============================================================

def costo_acumulado_nodo(nodo):
    """
    Suma jerarquica: Finca -> Lote -> Cultivo -> Insumo.
    CASO BASE: nodo sin hijos -> devuelve su valor.
    """
    if not nodo.tiene_hijos():
        return getattr(nodo, "valor", 0)

    total = getattr(nodo, "valor", 0)
    for hijo in nodo.hijos():
        total += costo_acumulado_nodo(hijo)
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
    nuevo_capital = capital + (precio_venta - costo_insumos)
    return capital_restante(mes + 1, nuevo_capital, precio_venta, costo_insumos)


def indice_vulnerabilidad_sucesion(miembro):
    """
    Suma acumulativa de vulnerabilidad en el arbol familiar.
    CASO BASE 1: miembro sin hijos -> devuelve su indice.
    CASO BASE 2: miembro marcado como joven -> devuelve su indice.
    Si tiene varios hijos, promedia sus indices.
    """
    if miembro is None:
        return 0.0
    if miembro.es_el_mas_joven() or not miembro.hijos:
        return miembro.indice
    indice_hijos = sum(
        indice_vulnerabilidad_sucesion(h) for h in miembro.hijos
    ) / len(miembro.hijos)
    return miembro.indice + indice_hijos