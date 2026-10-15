# ============================================================
# MiembroFamilia: nodo del arbol genealogico.
# La cadena es abuelo -> padre -> hijo, pero ahora cada miembro
# puede tener varios hijos porque se guardan en una lista.
# ============================================================

class MiembroFamilia:
    def __init__(self, nombre, indice, es_joven=False):
        if not nombre.strip():
            raise ValueError("El nombre del miembro no puede estar vacio.")
        if not (0.0 <= indice <= 1.0):
            raise ValueError("El indice debe estar entre 0.0 y 1.0.")
        self.nombre = nombre
        self.indice = indice
        self.hijos = []
        self.es_joven = es_joven

    def es_el_mas_joven(self):
        return self.es_joven

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)