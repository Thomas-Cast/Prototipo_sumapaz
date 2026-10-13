class MiembroFamilia:
    """
    Nodo del arbol genealogico familiar.
    Representa a un integrante: Abuelo, Padre, Hijo.

    El atributo 'indice' mide la vulnerabilidad acumulada del miembro
    (deudas, perdidas, falta de reinversion), en un rango de 0.0 a 1.0.

    El atributo 'hijo' enlaza con la siguiente generacion.
    El atributo 'es_joven' marca al miembro activo mas joven.

    Es el CASO BASE de la funcion recursiva
    indice_vulnerabilidad_sucesion: la cadena termina cuando se
    llega al miembro mas joven.
    """

    def __init__(self, nombre, indice, es_joven=False):
        self.nombre = nombre
        self.indice = max(0.0, min(1.0, indice))
        self.hijo = None
        self.es_joven = es_joven

    def es_el_mas_joven(self):
        return self.es_joven

    def __str__(self):
        marca = " (joven)" if self.es_joven else ""
        return f"{self.nombre}: indice {self.indice:.2f}{marca}"