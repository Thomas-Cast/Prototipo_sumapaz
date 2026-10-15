# ============================================================
# Pila: estructura LIFO.
# Se usa para mostrar como funciona la recursion internamente.
# ============================================================


class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, item):
        self.elementos.append(item)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def cima(self):
        if self.esta_vacia():
            return None
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamano(self):
        return len(self.elementos)