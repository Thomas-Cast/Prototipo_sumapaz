# ============================================================
# Familia: agrupa a los miembros que trabajan la finca.
# Una finca puede tener varias familias (aparceros, arrendatarios).
# Valida que solo exista un miembro joven, porque ese es el caso
# base de la recursion indice_vulnerabilidad_sucesion.
# ============================================================

from dominio.miembro_familia import MiembroFamilia

class Familia:
    def __init__(self, nombre):
        if not nombre.strip():
            raise ValueError("El nombre de la familia no puede estar vacio.")
        self.nombre = nombre
        self.raiz = None

    def agregar_miembro(self, nombre, indice, padre=None, es_joven=False):
        if es_joven and self._existe_joven():
            raise ValueError("Ya existe un miembro joven en esta familia.")
        nuevo = MiembroFamilia(nombre, indice, es_joven)
        if padre is None:
            if self.raiz is not None:
                raise ValueError(
                    "Ya existe una raiz. Indica el nombre del padre."
                )
            self.raiz = nuevo
        else:
            padre.agregar_hijo(nuevo)
        return nuevo

    def _existe_joven(self):
        """Recorrido BFS usando una cola propia."""
        from estructuras.cola import Cola
        if self.raiz is None:
            return False
        cola = Cola()
        cola.encolar(self.raiz)
        while not cola.esta_vacia():
            actual = cola.desencolar()
            if actual.es_joven:
                return True
            for h in actual.hijos:
                cola.encolar(h)
        return False

    def buscar_miembro(self, nombre):
        """Busqueda recursiva en el arbol familiar."""
        return self._buscar(self.raiz, nombre)

    def _buscar(self, miembro, nombre):
        if miembro is None:
            return None
        if miembro.nombre.lower() == nombre.lower():
            return miembro
        for h in miembro.hijos:
            encontrado = self._buscar(h, nombre)
            if encontrado:
                return encontrado
        return None

    def mostrar(self, miembro=None, nivel=0):
        if miembro is None:
            miembro = self.raiz
        if miembro is None:
            print("    (Sin miembros)")
            return
        marca = " [joven]" if miembro.es_joven else ""
        print("    " + "  " * nivel + f"- {miembro.nombre} ({miembro.indice:.2f}){marca}")
        for hijo in miembro.hijos:
            self.mostrar(hijo, nivel + 1)