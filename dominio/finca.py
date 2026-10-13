from dominio.lote import Lote


class Finca:
    """
    Raiz del arbol de costos.
    Representa la finca completa del productor.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.lotes = []

    def agregar_lote(self, nombre):
        self.lotes.append(Lote(nombre))

    def buscar_lote(self, nombre):
        for lote in self.lotes:
            if lote.nombre.lower() == nombre.lower():
                return lote
        return None

    def eliminar_lote(self, nombre):
        """Elimina un lote por nombre. Devuelve True si lo elimino."""
        lote = self.buscar_lote(nombre)
        if lote:
            self.lotes.remove(lote)
            return True
        return False

    def tiene_hijos(self):
        return len(self.lotes) > 0

    def __str__(self):
        return f"Finca: {self.nombre} ({len(self.lotes)} lotes)"