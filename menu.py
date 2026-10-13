# Menu principal del prototipo.
# Solo orquesta: llama a las clases del dominio y a los algoritmos.
# No implementa logica de negocio.

from dominio.finca import Finca
from dominio.miembro_familia import MiembroFamilia
from algoritmos.recursivos import (
    costo_acumulado_nodo,
    capital_restante,
    indice_vulnerabilidad_sucesion,
)
from algoritmos.iterativos import promedio_ph, almacen_mas_barato


class Menu:
    def __init__(self):
        self.finca = Finca("Finca Pekin")
        self.abuelo = MiembroFamilia("Abuelo", 0.3)
        self.padre = MiembroFamilia("Padre", 0.5)
        self.hijo = MiembroFamilia("Hijo", 0.8, es_joven=True)
        self.abuelo.hijo = self.padre
        self.padre.hijo = self.hijo

    def ejecutar(self):
        while True:
            print("\nPROTOTIPO SUMAPAZ - Fusagasuga")
            print("--------------------------------")
            print("1. Registrar lote")
            print("2. Agregar cultivo e insumos")
            print("3. Ver estructura de la finca")
            print("4. Calcular costo acumulado")
            print("5. Simular meses de supervivencia")
            print("6. Indice de vulnerabilidad sucesoral")
            print("7. Promedio de pH del suelo")
            print("8. Comparar precios de almacenes")
            print("0. Salir")
            print("--------------------------------")
            op = input("Opcion: ").strip()

            if op == "1":
                self._registrar_lote()
            elif op == "2":
                self._agregar_cultivo()
            elif op == "3":
                self._ver_finca()
            elif op == "4":
                self._costo()
            elif op == "5":
                self._supervivencia()
            elif op == "6":
                self._vulnerabilidad()
            elif op == "7":
                self._ph()
            elif op == "8":
                self._precios()
            elif op == "0":
                print("\nSaliendo del prototipo.\n")
                break
            else:
                print("Opcion invalida.")

    def _registrar_lote(self):
        nombre = input("Nombre del lote: ").strip()
        if not nombre:
            print("Nombre vacio.")
            return
        self.finca.agregar_lote(nombre)
        print(f"Lote '{nombre}' agregado.")

    def _agregar_cultivo(self):
        if not self.finca.lotes:
            print("Primero registra un lote.")
            return
        for i, lote in enumerate(self.finca.lotes, 1):
            print(f"  [{i}] {lote.nombre}")
        nombre = input("Nombre del lote: ").strip()
        lote = self.finca.buscar_lote(nombre)
        if not lote:
            print("Lote no encontrado.")
            return
        tipo = input("Tipo de cultivo (Mora/Tomate/Ornamentales): ").strip()
        lote.agregar_cultivo(tipo)
        cultivo = lote.cultivos[-1]

        while True:
            insumo = input("  Nombre del insumo (o 'fin'): ").strip()
            if insumo.lower() == "fin":
                break
            try:
                valor = float(input(f"  Valor de '{insumo}': "))
                if valor < 0:
                    print("  Valor negativo descartado.")
                    continue
                cultivo.agregar_insumo(insumo, valor)
                print("  Insumo agregado.")
            except ValueError:
                print("  Valor invalido.")

    def _ver_finca(self):
        print(f"\n{self.finca.nombre}")
        if not self.finca.lotes:
            print("  (Sin lotes)")
            return
        for lote in self.finca.lotes:
            print(f"  Lote: {lote.nombre}")
            if not lote.cultivos:
                print("    (sin cultivos)")
            for cultivo in lote.cultivos:
                print(f"    Cultivo: {cultivo.nombre}")
                for insumo in cultivo.insumos:
                    print(f"      - {insumo.nombre}: ${insumo.valor:,.0f}")

    def _costo(self):
        total = costo_acumulado_nodo(self.finca)
        print(f"\nCosto acumulado: ${total:,.0f}")
        try:
            venta = float(input("Precio de venta estimado: $"))
            if venta > 0:
                margen = venta - total
                if margen > 0:
                    print(f"Margen proyectado: ${margen:,.0f} (rentable)")
                else:
                    print(f"Margen proyectado: ${margen:,.0f} (perdida)")
        except ValueError:
            print("No se calculo margen.")

    def _supervivencia(self):
        try:
            capital = float(input("Capital inicial: "))
            precio = float(input("Ingreso mensual: "))
            costo = float(input("Costo mensual: "))
        except ValueError:
            print("Datos invalidos.")
            return

        if capital <= 0:
            print("\nEl productor ya esta en quiebra (capital <= 0).")
            return
        if precio <= costo:
            print("\nAlerta: el ingreso no cubre los costos. Quiebra progresiva.")

        meses = capital_restante(1, capital, precio, costo)
        if meses >= 24:
            print("\nSe mantiene al menos 24 meses.")
            print("Situacion estable.")
        else:
            print(f"\nQuiebra en el mes {meses}.")
            if meses < 6:
                print("Riesgo critico: busca reducir costos o diversificar.")
            elif meses < 12:
                print("Riesgo medio: revisa tus costos mensuales.")
            else:
                print("Riesgo bajo: aun tienes margen de maniobra.")

    def _vulnerabilidad(self):
        indice = indice_vulnerabilidad_sucesion(self.abuelo)
        print(f"\nIndice de vulnerabilidad: {indice:.2f}")
        if indice >= 1.5:
            print("Riesgo ALTO. Se recomienda apoyo tecnico y crediticio.")
        elif indice >= 1.0:
            print("Riesgo MEDIO. Se recomienda capacitacion en costos.")
        else:
            print("Riesgo BAJO.")

    def _ph(self):
        entrada = input("Muestras de pH separadas por coma: ").strip()
        try:
            muestras = [float(x) for x in entrada.split(",")]
        except ValueError:
            print("Datos invalidos.")
            return
        ph = promedio_ph(muestras)
        if ph is None:
            print("Sin muestras validas.")
            return
        print(f"\nPH promedio: {ph:.2f}")
        if ph < 5.5:
            dosis = (5.5 - ph) * 1000
            print(f"ALERTA: pH bajo. Aplicar aproximadamente {dosis:.0f} kg de cal por hectarea.")
        else:
            print("pH adecuado. No requiere cal.")

    def _precios(self):
        print("Ingresa nombre,precio. Escribe 'fin' para terminar.")
        precios = []
        while True:
            linea = input("  > ").strip()
            if linea.lower() == "fin":
                break
            try:
                n, p = linea.split(",")
                precios.append((n.strip(), float(p)))
            except ValueError:
                print("Formato invalido.")

        mejor, valor = almacen_mas_barato(precios)
        if mejor:
            print(f"\nMas barato: {mejor} (${valor:,.0f})")
            validos = [p for _, p in precios if isinstance(p, (int, float)) and p > 0]
            if validos:
                mas_caro = max(validos)
                ahorro = mas_caro - valor
                print(f"Ahorro frente al mas caro: ${ahorro:,.0f}")
        else:
            print("Sin precios validos.")
