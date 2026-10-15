# ============================================================
# Insumo: hoja del arbol de costos.
# Caso base de la recursion costo_acumulado_nodo.
# ============================================================

class Insumo:
    def __init__(self, nombre, valor):
        if not nombre.strip():
            raise ValueError("El nombre del insumo no puede estar vacio.")
        if valor < 0:
            raise ValueError("El valor del insumo no puede ser negativo.")
        self.nombre = nombre
        self.valor = valor

    def tiene_hijos(self):
        return False

    def hijos(self):
        return []

    def __repr__(self):
        return f"Insumo({self.nombre}, {self.valor})"