# ============================================================
# Lote: nodo intermedio de la finca.
# Cada lote tiene sus propios cultivos y sus propias muestras
# de pH, porque el pH es una propiedad del suelo, no de la finca.
# ============================================================

class Lote:
    def __init__(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre del lote no puede estar vacio.")
        self.nombre = nombre
        self.cultivos = []
        self.muestras_ph = []

    def agregar_cultivo(self, cultivo):
        for c in self.cultivos:
            if c.nombre.lower() == cultivo.nombre.lower():
                raise ValueError(
                    f"El cultivo '{cultivo.nombre}' ya existe en este lote."
                )
        self.cultivos.append(cultivo)

    def agregar_muestra_ph(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("La muestra de pH debe ser numerica.")
        if not (0 < valor < 14):
            raise ValueError("La muestra de pH debe estar entre 0 y 14.")
        self.muestras_ph.append(valor)

    def tiene_hijos(self):
        return len(self.cultivos) > 0

    def hijos(self):
        return self.cultivos