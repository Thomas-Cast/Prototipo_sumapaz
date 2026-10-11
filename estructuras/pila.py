class Pila:
    """
    Estructura LIFO: el ultimo en entrar es el primero en salir.

    Se usa en el prototipo para modelar la pila de llamadas
    que la recursion genera internamente, y para recorridos
    en profundidad sobre el arbol de la finca.
    """

    def __init__(self):
        self.elementos = []

    def apilar(self, item):
        """Agrega un elemento a la cima de la pila."""
        self.elementos.append(item)

    def desapilar(self):
        """Saca y devuelve el elemento de la cima. None si esta vacia."""
        if not self.esta_vacia():
            return self.elementos.pop()
        return None

    def esta_vacia(self):
        """Devuelve True si la pila no tiene elementos."""
        return len(self.elementos) == 0

    def cima(self):
        """Devuelve el elemento de la cima sin sacarlo."""
        if not self.esta_vacia():
            return self.elementos[-1]
        return None

    def tamano(self):
        """Devuelve cuantos elementos tiene la pila."""
        return len(self.elementos)
