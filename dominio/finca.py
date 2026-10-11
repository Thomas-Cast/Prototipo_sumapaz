from dominio.lote import Lote


class Finca:
    """
    Raiz del arbol de costos.
    Representa la finca completa del productor.

    Contiene una lista de lotes.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.lotes = []

    def agregar_lote(self, nombre):
        """Agrega un lote a la finca."""
        self.lotes.append(Lote(nombre))

    def buscar_lote(self, nombre):
        """Busca un lote por nombre. Devuelve el lote o None."""
        for lote in self.lotes:
            if lote.nombre.lower() == nombre.lower():
                return lote
        return None

    def tiene_hijos(self):
        """Devuelve True si tiene al menos un lote."""
        return len(self.lotes) > 0

    def __str__(self):
        return f"Finca: {self.nombre} ({len(self.lotes)} lotes)"
