class ArbolGenealogico:
    """
    Contenedor del arbol familiar.
    Guarda la raiz (el miembro mas antiguo) y expone
    operaciones basicas sobre la cadena.
    """

    def __init__(self, raiz):
        self.raiz = raiz

    def miembros(self):
        lista = []
        actual = self.raiz
        while actual is not None:
            lista.append(actual)
            actual = actual.hijo
        return lista

    def tamano(self):
        return len(self.miembros())

    def __str__(self):
        return f"Arbol genealogico con {self.tamano()} miembros"