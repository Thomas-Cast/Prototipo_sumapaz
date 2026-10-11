class Insumo:
    """
    Hoja del arbol de costos.
    Representa un gasto individual: fertilizante, jornal, cal, etc.

    Es el CASO BASE de la funcion recursiva costo_acumulado_nodo,
    porque no tiene hijos.
    """

    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def tiene_hijos(self):
        """Devuelve False: un insumo nunca tiene hijos."""
        return False

    def __str__(self):
        return f"{self.nombre}: ${self.valor:,.0f}"
