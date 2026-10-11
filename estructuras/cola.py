class Cola:
    """
    Estructura FIFO: el primero en entrar es el primero en salir.

    Se usa en el prototipo para recorrer el arbol de la finca
    por niveles (Finca, luego Lotes, luego Cultivos, luego Insumos).
    """

    def __init__(self):
        self.elementos = []

    def encolar(self, item):
        """Agrega un elemento al final de la cola."""
        self.elementos.append(item)

    def desencolar(self):
        """Saca y devuelve el primer elemento. None si esta vacia."""
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None

    def esta_vacia(self):
        """Devuelve True si la cola no tiene elementos."""
        return len(self.elementos) == 0

    def frente(self):
        """Devuelve el primer elemento sin sacarlo."""
        if not self.esta_vacia():
            return self.elementos[0]
        return None

    def tamano(self):
        """Devuelve cuantos elementos tiene la cola."""
        return len(self.elementos)
