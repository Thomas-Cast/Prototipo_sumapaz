# ============================================================
# Cultivo: nodo intermedio del arbol de costos.
# Conoce su rango optimo de pH y la dosis de cal sugerida.
# ============================================================

from dominio.insumo import Insumo

class Cultivo:
    # Rango optimo de pH y dosis base de cal por planta (AGROSAVIA)
    PH_OPTIMO = {
        "mora":         (5.5, 6.5, 200),
        "tomate":       (5.8, 6.8, 300),
        "ornamentales": (5.5, 7.0, 150),
    }

    def __init__(self, nombre):
        if not nombre.strip():
            raise ValueError("El tipo de cultivo no puede estar vacio.")
        if nombre.lower() not in self.PH_OPTIMO:
            raise ValueError(
                f"Tipo invalido. Use: {', '.join(self.PH_OPTIMO)}"
            )
        self.nombre = nombre
        self.insumos = []

    def agregar_insumo(self, insumo):
        for i in self.insumos:
            if i.nombre.lower() == insumo.nombre.lower():
                raise ValueError(f"El insumo '{insumo.nombre}' ya existe.")
        self.insumos.append(insumo)

    def tiene_hijos(self):
        return len(self.insumos) > 0

    def hijos(self):
        return self.insumos

    def rango_ph(self):
        return self.PH_OPTIMO.get(self.nombre.lower())

    def dosis_cal(self, ph_actual):
        """
        Gramos de cal por planta segun el deficit de pH.
        Si el pH esta dentro del rango optimo, devuelve 0.
        """
        rango = self.rango_ph()
        if rango is None:
            return 0
        minimo, _, dosis_base = rango
        if ph_actual >= minimo:
            return 0
        deficit = minimo - ph_actual
        return int(dosis_base * (1 + deficit))