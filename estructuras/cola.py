# ============================================================
# Cola: estructura FIFO.
# Se usa para el recorrido por niveles del arbol familiar
# y para verificar si ya existe un miembro joven.
# ============================================================

class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, item):
        self.elementos.append(item)

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop(0)

    def frente(self):
        if self.esta_vacia():
            return None
        return self.elementos[0]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamano(self):
        return len(self.elementos)