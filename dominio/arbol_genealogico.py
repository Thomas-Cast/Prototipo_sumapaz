class ArbolGenealogico:
    """
    Contenedor del arbol familiar.
    Guarda la raiz (el miembro mas antiguo) y expone
    operaciones basicas sobre la cadena.

    No implementa la recursion: eso lo hace la funcion
    indice_vulnerabilidad_sucesion en algoritmos/recursivos.py.
    """

    def __init__(self, raiz):
        self.raiz = raiz

    def miembros(self):
        """Devuelve la lista de miembros desde la raiz hasta el mas joven."""
        lista = []
        actual = self.raiz
        while actual is not None:
            lista.append(actual)
            actual = actual.hijo
        return lista

    def tamano(self):
        """Devuelve cuantos miembros tiene la cadena."""
        return len(self.miembros())

    def __str__(self):
        return f"Arbol genealogico con {self.tamano()} miembros"
