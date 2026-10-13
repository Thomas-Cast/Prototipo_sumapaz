class Pila:
    """
    Estructura LIFO: el ultimo en entrar es el primero en salir.
    """

    def __init__(self):
        self.elementos = []

    def apilar(self, item):
        self.elementos.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.elementos.pop()
        return None

    def esta_vacia(self):
        return len(self.elementos) == 0

    def cima(self):
        if not self.esta_vacia():
            return self.elementos[-1]
        return None

    def tamano(self):
        return len(self.elementos)