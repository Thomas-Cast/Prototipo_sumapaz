# Punto de entrada del prototipo Sumapaz.
# Este archivo NO se modifica: solo llama al menu.

import sys
sys.setrecursionlimit(2000)

from menu import Menu

if __name__ == "__main__":
    app = Menu()
    app.ejecutar()
