from dominio.insumo import Insumo


class Cultivo:
    """
    Nodo intermedio del arbol de costos.
    Representa un cultivo: Mora, Tomate u Ornamentales.

    Puede tener varios insumos asociados.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.insumos = []

    def agregar_insumo(self, nombre, valor):
        """Agrega un insumo al cultivo."""
        self.insumos.append(Insumo(nombre, valor))

    def tiene_hijos(self):
        """Devuelve True si tiene al menos un insumo."""
        return len(self.insumos) > 0

    def __str__(self):
        return f"Cultivo: {self.nombre} ({len(self.insumos)} insumos)"
