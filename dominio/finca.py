# ============================================================
# Finca: raiz del arbol de costos.
# Contiene lotes y familias. Un productor puede tener varias fincas.
# La familia esta vinculada a la finca porque es la que le da
# continuidad al predio.
# ============================================================

class Finca:
    def __init__(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre de la finca no puede estar vacio.")
        self.nombre = nombre
        self.lotes = []
        self.familias = []

    def agregar_lote(self, lote):
        for l in self.lotes:
            if l.nombre.lower() == lote.nombre.lower():
                raise ValueError(f"El lote '{lote.nombre}' ya existe.")
        self.lotes.append(lote)

    def agregar_familia(self, familia):
        for f in self.familias:
            if f.nombre.lower() == familia.nombre.lower():
                raise ValueError(f"La familia '{familia.nombre}' ya existe.")
        self.familias.append(familia)

    def buscar_lote(self, nombre):
        for l in self.lotes:
            if l.nombre.lower() == nombre.lower():
                return l
        return None

    def buscar_familia(self, nombre):
        for f in self.familias:
            if f.nombre.lower() == nombre.lower():
                return f
        return None

    def tiene_hijos(self):
        return len(self.lotes) > 0

    def hijos(self):
        return self.lotes