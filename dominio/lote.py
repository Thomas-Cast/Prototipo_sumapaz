from dominio.cultivo import Cultivo


class Lote:
    """
    Nodo intermedio del arbol de costos.
    Representa una division de la finca.

    Puede tener varios cultivos.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.cultivos = []

    def agregar_cultivo(self, nombre):
        """Agrega un cultivo al lote."""
        self.cultivos.append(Cultivo(nombre))

    def tiene_hijos(self):
        """Devuelve True si tiene al menos un cultivo."""
        return len(self.cultivos) > 0

    def __str__(self):
        return f"Lote: {self.nombre} ({len(self.cultivos)} cultivos)"
