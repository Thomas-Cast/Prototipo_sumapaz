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
        nombre = input("Nombre de la finca: ").strip()
        if not nombre:
            nombre = "Mi finca"
        self.finca = Finca(nombre)
        self.raiz_familiar = None

    # =========================================================
    # MENU PRINCIPAL
    # =========================================================
    def ejecutar(self):
        while True:
            print(f"\nPROTOTIPO SUMAPAZ - Fusagasuga")
            print(f"Finca: {self.finca.nombre}\n")
            print("1. Registrar lote")
            print("2. Agregar cultivo e insumos")
            print("3. Ver estructura de la finca")
            print("4. Calcular costo acumulado")
            print("5. Simular meses de supervivencia")
            print("6. Registrar familia y calcular vulnerabilidad")
            print("7. Promedio de pH del suelo")
            print("8. Comparar precios de almacenes")
            print("9. Eliminar lote")
            print("10. Eliminar cultivo")
            print("11. Eliminar insumo")
            print("12. Cambiar nombre de la finca")
            print("0. Salir\n")
            op = input("Opcion: ").strip()

            if op == "1":
                self._registrar_lote()
            elif op == "2":
                self._submenu_agregar()
            elif op == "3":
                self._submenu_ver()
            elif op == "4":
                self._costo()
            elif op == "5":
                self._supervivencia()
            elif op == "6":
                self._submenu_familia()
            elif op == "7":
                self._ph()
            elif op == "8":
                self._precios()
            elif op == "9":
                self._eliminar_lote()
            elif op == "10":
                self._eliminar_cultivo()
            elif op == "11":
                self._eliminar_insumo()
            elif op == "12":
                self._cambiar_nombre_finca()
            elif op == "0":
                confirmar = input("Estas seguro de salir? (s/n): ").strip().lower()
                if confirmar == "s":
                    print("\nSaliendo del prototipo.\n")
                    break
            else:
                print("Opcion invalida.")

    # =========================================================
    # SUBMENU: AGREGAR CULTIVO E INSUMOS
    # =========================================================
    def _submenu_agregar(self):
        lote = self._elegir_lote()
        if not lote:
            return

        tipo = input("Nombre del cultivo: ").strip()
        if not tipo:
            print("Nombre vacio.")
            return

        insumos_temporales = []

        while True:
            print(f"\nCultivo: {tipo} en Lote: {lote.nombre}")
            print(f"Insumos agregados: {len(insumos_temporales)}\n")
            print("1. Agregar insumo")
            print("2. Ver insumos agregados")
            print("3. Eliminar un insumo")
            print("4. Terminar y guardar cultivo")
            print("0. Cancelar\n")
            op = input("Opcion: ").strip()

            if op == "1":
                insumo = input("  Nombre del insumo: ").strip()
                if not insumo:
                    print("  Nombre vacio.")
                    continue
                valor = self._pedir_numero(f"  Valor de '{insumo}': ")
                if valor is None or valor <= 0:
                    print("  Valor invalido.")
                    continue
                insumos_temporales.append((insumo, valor))
                print("  Insumo agregado temporalmente.")

            elif op == "2":
                if not insumos_temporales:
                    print("  (Sin insumos)")
                else:
                    for i, (n, v) in enumerate(insumos_temporales, 1):
                        print(f"  [{i}] {n}: ${v:,.0f}")

            elif op == "3":
                if not insumos_temporales:
                    print("  No hay insumos para eliminar.")
                    continue
                for i, (n, v) in enumerate(insumos_temporales, 1):
                    print(f"  [{i}] {n}: ${v:,.0f}")
                try:
                    idx = int(input("  Numero del insumo a eliminar: ")) - 1
                    if 0 <= idx < len(insumos_temporales):
                        eliminado = insumos_temporales.pop(idx)
                        print(f"  Eliminado: {eliminado[0]}")
                    else:
                        print("  Numero fuera de rango.")
                except ValueError:
                    print("  Numero invalido.")

            elif op == "4":
                if not insumos_temporales:
                    confirmar = input("No hay insumos. Guardar cultivo vacio? (s/n): ").strip().lower()
                    if confirmar != "s":
                        continue
                lote.agregar_cultivo(tipo)
                cultivo = lote.cultivos[-1]
                for n, v in insumos_temporales:
                    cultivo.agregar_insumo(n, v)
                print(f"\nCultivo '{tipo}' guardado en '{lote.nombre}' con {len(insumos_temporales)} insumos.")
                return

            elif op == "0":
                print("Cancelado. No se guardo el cultivo.")
                return

            else:
                print("Opcion invalida.")

    # =========================================================
    # SUBMENU: VER ESTRUCTURA
    # =========================================================
    def _submenu_ver(self):
        while True:
            print("\nVer estructura\n")
            print("1. Ver toda la finca")
            print("2. Ver un lote")
            print("3. Ver un cultivo")
            print("0. Volver al menu principal\n")
            op = input("Opcion: ").strip()

            if op == "1":
                self._ver_finca_completa()
            elif op == "2":
                self._ver_un_lote()
            elif op == "3":
                self._ver_un_cultivo()
            elif op == "0":
                return
            else:
                print("Opcion invalida.")

    def _ver_finca_completa(self):
        print(f"\n{self.finca.nombre}")
        if not self.finca.lotes:
            print("  (Sin lotes)")
            return
        total_finca = 0
        for lote in self.finca.lotes:
            print(f"  Lote: {lote.nombre}")
            if not lote.cultivos:
                print("    (sin cultivos)")
            subtotal_lote = 0
            for cultivo in lote.cultivos:
                print(f"    Cultivo: {cultivo.nombre}")
                if not cultivo.insumos:
                    print("      (sin insumos: costo 0)")
                subtotal_cultivo = 0
                for insumo in cultivo.insumos:
                    print(f"      - {insumo.nombre}: ${insumo.valor:,.0f}")
                    subtotal_cultivo += insumo.valor
                print(f"      Subtotal cultivo: ${subtotal_cultivo:,.0f}")
                subtotal_lote += subtotal_cultivo
            print(f"    Subtotal lote: ${subtotal_lote:,.0f}")
            total_finca += subtotal_lote
        print(f"  Total finca: ${total_finca:,.0f}")

    def _ver_un_lote(self):
        lote = self._elegir_lote()
        if not lote:
            return
        print(f"\nLote: {lote.nombre}")
        if not lote.cultivos:
            print("  (sin cultivos)")
            return
        subtotal = 0
        for cultivo in lote.cultivos:
            print(f"  Cultivo: {cultivo.nombre}")
            if not cultivo.insumos:
                print("    (sin insumos)")
            subtotal_cultivo = 0
            for insumo in cultivo.insumos:
                print(f"    - {insumo.nombre}: ${insumo.valor:,.0f}")
                subtotal_cultivo += insumo.valor
            print(f"    Subtotal cultivo: ${subtotal_cultivo:,.0f}")
            subtotal += subtotal_cultivo
        print(f"  Subtotal lote: ${subtotal:,.0f}")

    def _ver_un_cultivo(self):
        lote = self._elegir_lote()
        if not lote or not lote.cultivos:
            print("Ese lote no tiene cultivos.")
            return
        for i, c in enumerate(lote.cultivos, 1):
            print(f"  [{i}] {c.nombre}")
        nombre = input("Nombre del cultivo: ").strip()
        cultivo = None
        for c in lote.cultivos:
            if c.nombre.lower() == nombre.lower():
                cultivo = c
                break
        if not cultivo:
            print("Cultivo no encontrado.")
            return
        print(f"\nCultivo: {cultivo.nombre} (Lote: {lote.nombre})")
        if not cultivo.insumos:
            print("  (sin insumos)")
            return
        subtotal = 0
        for insumo in cultivo.insumos:
            print(f"  - {insumo.nombre}: ${insumo.valor:,.0f}")
            subtotal += insumo.valor
        print(f"  Subtotal: ${subtotal:,.0f}")

    # =========================================================
    # SUBMENU: FAMILIA
    # =========================================================
    def _submenu_familia(self):
        miembros = []

        while True:
            print(f"\nRegistrar familia")
            print(f"Miembros registrados: {len(miembros)}\n")
            print("1. Agregar miembro")
            print("2. Ver miembros")
            print("3. Eliminar miembro")
            print("4. Terminar y calcular vulnerabilidad")
            print("0. Cancelar\n")
            op = input("Opcion: ").strip()

            if op == "1":
                nombre = input("  Nombre del miembro: ").strip()
                if not nombre:
                    print("  Nombre vacio.")
                    continue
                indice = self._pedir_numero(f"  Indice de {nombre} (0.0 a 1.0): ")
                if indice is None or indice < 0 or indice > 1:
                    print("  Indice invalido.")
                    continue
                joven = input(f"  {nombre} es el mas joven? (s/n): ").strip().lower() == "s"
                miembros.append((nombre, indice, joven))
                print("  Miembro agregado.")

            elif op == "2":
                if not miembros:
                    print("  (Sin miembros)")
                else:
                    for i, (n, idx, j) in enumerate(miembros, 1):
                        marca = " (joven)" if j else ""
                        print(f"  [{i}] {n}: {idx:.2f}{marca}")

            elif op == "3":
                if not miembros:
                    print("  No hay miembros para eliminar.")
                    continue
                for i, (n, idx, j) in enumerate(miembros, 1):
                    print(f"  [{i}] {n}")
                try:
                    pos = int(input("  Numero del miembro a eliminar: ")) - 1
                    if 0 <= pos < len(miembros):
                        eliminado = miembros.pop(pos)
                        print(f"  Eliminado: {eliminado[0]}")
                    else:
                        print("  Numero fuera de rango.")
                except ValueError:
                    print("  Numero invalido.")

            elif op == "4":
                if not miembros:
                    print("  No hay miembros registrados.")
                    continue
                if not any(j for _, _, j in miembros):
                    confirmar = input("  Ningun miembro marcado como joven. Continuar? (s/n): ").strip().lower()
                    if confirmar != "s":
                        continue

                raiz = None
                anterior = None
                for n, idx, j in miembros:
                    m = MiembroFamilia(n, idx, es_joven=j)
                    if raiz is None:
                        raiz = m
                    else:
                        anterior.hijo = m
                    anterior = m
                self.raiz_familiar = raiz

                indice_total = indice_vulnerabilidad_sucesion(raiz)
                print(f"\nIndice de vulnerabilidad sucesoral: {indice_total:.2f}")
                if indice_total >= 1.5:
                    print("Riesgo ALTO. Se recomienda apoyo tecnico y crediticio.")
                elif indice_total >= 1.0:
                    print("Riesgo MEDIO. Se recomienda capacitacion en costos.")
                else:
                    print("Riesgo BAJO.")
                return

            elif op == "0":
                print("Cancelado. No se guardo la familia.")
                return

            else:
                print("Opcion invalida.")

    # =========================================================
    # UTILIDADES INTERNAS
    # =========================================================
    def _pedir_numero(self, mensaje):
        entrada = input(mensaje).strip().replace(",", ".")
        try:
            return float(entrada)
        except ValueError:
            return None

    def _elegir_lote(self):
        if not self.finca.lotes:
            print("No hay lotes registrados.")
            return None
        for i, lote in enumerate(self.finca.lotes, 1):
            print(f"  [{i}] {lote.nombre}")
        nombre = input("Nombre del lote: ").strip()
        lote = self.finca.buscar_lote(nombre)
        if not lote:
            print("Lote no encontrado.")
        return lote

    # =========================================================
    # OPCIONES SIMPLES
    # =========================================================
    def _registrar_lote(self):
        nombre = input("Nombre del lote: ").strip()
        if not nombre:
            print("Nombre vacio.")
            return
        if self.finca.buscar_lote(nombre):
            print("Ya existe un lote con ese nombre.")
            return
        self.finca.agregar_lote(nombre)
        print(f"Lote '{nombre}' agregado.")

    def _costo(self):
        if not self.finca.lotes:
            print("\nPrimero registra lotes e insumos.")
            return
        total = costo_acumulado_nodo(self.finca)
        print(f"\nCosto acumulado: ${total:,.0f}")
        if total == 0:
            print("No hay insumos registrados.")
            return
        venta = self._pedir_numero("Precio de venta estimado: $")
        if venta is None or venta <= 0:
            print("No se calculo margen.")
            return
        margen = venta - total
        if margen > 0:
            print(f"Margen proyectado: ${margen:,.0f} (rentable)")
        else:
            print(f"Margen proyectado: ${margen:,.0f} (perdida)")

    def _supervivencia(self):
        capital = self._pedir_numero("Capital inicial: ")
        precio = self._pedir_numero("Ingreso mensual: ")
        costo = self._pedir_numero("Costo mensual: ")
        if capital is None or precio is None or costo is None:
            print("Datos invalidos.")
            return

        if capital <= 0:
            print("\nEl productor ya esta en quiebra (capital <= 0).")
            return
        if precio <= costo:
            print("\nAlerta: el ingreso no cubre los costos. Quiebra progresiva.")

        print("\nProyeccion mes a mes:")
        self._proyectar(1, capital, precio, costo)

    def _proyectar(self, mes, capital, precio, costo):
        if capital <= 0:
            print(f"  Mes {mes - 1}: ${capital:,.0f} -> QUIEBRA")
            print(f"\nQuiebra en el mes {mes - 1}.")
            if mes - 1 < 6:
                print("Riesgo critico: busca reducir costos o diversificar.")
            elif mes - 1 < 12:
                print("Riesgo medio: revisa tus costos mensuales.")
            else:
                print("Riesgo bajo: aun tienes margen de maniobra.")
            return
        if mes == 25:
            print(f"  Mes 24: ${capital:,.0f}")
            print("\nSe mantiene al menos 24 meses. Situacion estable.")
            return
        print(f"  Mes {mes}: ${capital:,.0f}")
        nuevo = capital + (precio - costo)
        self._proyectar(mes + 1, nuevo, precio, costo)

    def _ph(self):
        entrada = input("Muestras de pH separadas por coma: ").strip()
        try:
            muestras = [float(x.replace(",", ".")) for x in entrada.split(",")]
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
            print(f"ALERTA: pH bajo. Aplicar ~{dosis:.0f} kg de cal por hectarea.")
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
                precio = float(p.strip().replace(",", "."))
                if precio <= 0:
                    print("Precio invalido.")
                    continue
                precios.append((n.strip(), precio))
            except ValueError:
                print("Formato invalido.")

        mejor, valor = almacen_mas_barato(precios)
        if mejor:
            print(f"\nMas barato: {mejor} (${valor:,.0f})")
            validos = [p for _, p in precios if isinstance(p, (int, float)) and p > 0]
            if validos:
                mas_caro = max(validos)
                ahorro = mas_caro - valor
                porcentaje = (ahorro / mas_caro) * 100 if mas_caro > 0 else 0
                print(f"Ahorro frente al mas caro: ${ahorro:,.0f} ({porcentaje:.1f}%)")
        else:
            print("Sin precios validos.")

    def _eliminar_lote(self):
        lote = self._elegir_lote()
        if not lote:
            return
        confirmar = input(f"Eliminar lote '{lote.nombre}'? (s/n): ").strip().lower()
        if confirmar == "s":
            self.finca.eliminar_lote(lote.nombre)
            print(f"Lote '{lote.nombre}' eliminado.")
        else:
            print("Cancelado.")

    def _eliminar_cultivo(self):
        lote = self._elegir_lote()
        if not lote or not lote.cultivos:
            print("Ese lote no tiene cultivos.")
            return
        for i, c in enumerate(lote.cultivos, 1):
            print(f"  [{i}] {c.nombre}")
        nombre = input("Nombre del cultivo a eliminar: ").strip()
        cultivo = None
        for c in lote.cultivos:
            if c.nombre.lower() == nombre.lower():
                cultivo = c
                break
        if not cultivo:
            print("Cultivo no encontrado.")
            return
        confirmar = input(f"Eliminar cultivo '{cultivo.nombre}'? (s/n): ").strip().lower()
        if confirmar == "s":
            lote.cultivos.remove(cultivo)
            print(f"Cultivo '{cultivo.nombre}' eliminado.")
        else:
            print("Cancelado.")

    def _eliminar_insumo(self):
        lote = self._elegir_lote()
        if not lote or not lote.cultivos:
            print("Ese lote no tiene cultivos.")
            return
        for i, c in enumerate(lote.cultivos, 1):
            print(f"  [{i}] {c.nombre}")
        nombre_cultivo = input("Nombre del cultivo: ").strip()
        cultivo = None
        for c in lote.cultivos:
            if c.nombre.lower() == nombre_cultivo.lower():
                cultivo = c
                break
        if not cultivo or not cultivo.insumos:
            print("Cultivo no encontrado o sin insumos.")
            return
        for i, ins in enumerate(cultivo.insumos, 1):
            print(f"  [{i}] {ins.nombre}: ${ins.valor:,.0f}")
        nombre_insumo = input("Nombre del insumo a eliminar: ").strip()
        insumo = None
        for ins in cultivo.insumos:
            if ins.nombre.lower() == nombre_insumo.lower():
                insumo = ins
                break
        if not insumo:
            print("Insumo no encontrado.")
            return
        confirmar = input(f"Eliminar insumo '{insumo.nombre}'? (s/n): ").strip().lower()
        if confirmar == "s":
            cultivo.insumos.remove(insumo)
            print(f"Insumo '{insumo.nombre}' eliminado.")
        else:
            print("Cancelado.")

    def _cambiar_nombre_finca(self):
        print(f"Nombre actual: {self.finca.nombre}")
        nuevo = input("Nuevo nombre: ").strip()
        if not nuevo:
            print("Nombre vacio. No se cambio.")
            return
        self.finca.nombre = nuevo
        print(f"Nombre cambiado a '{nuevo}'.")