class Cola:
    """
    Estructura FIFO: el primero en entrar es el primero en salir.
    """

    def __init__(self):
        self.elementos = []

    def encolar(self, item):
        self.elementos.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None

    def esta_vacia(self):
        return len(self.elementos)