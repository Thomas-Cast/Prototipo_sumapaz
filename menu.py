# ============================================================
# Menu interactivo del prototipo Sumapaz.
# Aqui vive la clase PrototipoSumapaz con toda la interaccion
# con el usuario y las validaciones de entrada.
# ============================================================

from dominio.finca import Finca
from dominio.lote import Lote
from dominio.cultivo import Cultivo
from dominio.insumo import Insumo
from dominio.familia import Familia

from algoritmos.recursivos import (
    costo_acumulado_nodo,
    capital_restante,
    indice_vulnerabilidad_sucesion,
)
from algoritmos.iterativos import (
    promedio_ph,
    almacen_mas_barato_por_producto,
)


# ============================================================
# Utilidades de entrada estandarizadas
# ============================================================

def pedir(mensaje, tipo=float, minimo=None, maximo=None, permitir_vacio=False):
    """Solicita un dato al usuario y lo valida en un solo lugar."""
    while True:
        valor = input(mensaje).strip()
        if not permitir_vacio and valor == "":
            print("  No puede estar vacio.")
            continue
        if tipo is str:
            return valor
        try:
            numero = tipo(valor)
        except ValueError:
            print(f"  Debe ser {tipo.__name__}.")
            continue
        if minimo is not None and numero < minimo:
            print(f"  Debe ser mayor o igual a {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            print(f"  Debe ser menor o igual a {maximo}.")
            continue
        return numero


def pedir_si_no(mensaje):
    """Solicita confirmacion s/n y devuelve bool."""
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("s", "si", "n", "no"):
            return valor in ("s", "si")
        print("  Responde 's' o 'n'.")


# ============================================================
# Clase principal del menu
# ============================================================

class PrototipoSumapaz:
    def __init__(self):
        self.fincas = []
        self.finca_actual = None

    # ---------- MENU ----------
    def menu(self):
        while True:
            print("   PROTOTIPO SUMAPAZ - Fusagasuga")
            if self.finca_actual:
                print(f"   Finca activa: {self.finca_actual.nombre}")
            print("1. Crear finca")
            print("2. Seleccionar finca activa")
            print("3. Ver fincas")
            print("4. Registrar lote")
            print("5. Registrar familia")
            print("6. Agregar miembro a una familia")
            print("7. Agregar cultivo e insumos a un lote")
            print("8. Registrar muestras de pH de un lote")
            print("9. Ver estructura completa")
            print("10. Calcular costo acumulado")
            print("11. Simular supervivencia")
            print("12. Vulnerabilidad sucesoral")
            print("13. Comparar precios por producto")
            print("14. Generar alertas")
            print("0. Salir")
            opcion = input("\nElige una opcion: ").strip()

            acciones = {
                "1": self.crear_finca,
                "2": self.seleccionar_finca,
                "3": self.ver_fincas,
                "4": self.registrar_lote,
                "5": self.registrar_familia,
                "6": self.agregar_miembro,
                "7": self.agregar_cultivo,
                "8": self.registrar_ph,
                "9": self.ver_estructura,
                "10": self.calcular_costo,
                "11": self.simular_supervivencia,
                "12": self.calcular_vulnerabilidad,
                "13": self.comparar_precios,
                "14": self.generar_alertas,
            }
            if opcion == "0":
                print("\nSaliendo del prototipo Sumapaz...\n")
                break
            accion = acciones.get(opcion)
            if accion:
                accion()
            else:
                print("  Opcion invalida.")

    # ---------- FINCAS ----------
    def _requiere_finca(self):
        if not self.finca_actual:
            print("  Primero crea o selecciona una finca.")
            return False
        return True

    def crear_finca(self):
        nombre = pedir("Nombre de la finca: ", tipo=str)
        try:
            nueva = Finca(nombre)
            self.fincas.append(nueva)
            self.finca_actual = nueva
            print(f"  Finca '{nombre}' creada y seleccionada.")
        except ValueError as e:
            print(f"  {e}")

    def seleccionar_finca(self):
        if not self.fincas:
            print("  No hay fincas creadas.")
            return
        for i, f in enumerate(self.fincas, 1):
            print(f"  [{i}] {f.nombre}")
        nombre = pedir("Nombre de la finca: ", tipo=str)
        finca = next(
            (f for f in self.fincas if f.nombre.lower() == nombre.lower()),
            None,
        )
        if finca:
            self.finca_actual = finca
            print(f"  Finca activa: {finca.nombre}")
        else:
            print("  Finca no encontrada.")

    def ver_fincas(self):
        if not self.fincas:
            print("  No hay fincas creadas.")
            return
        for f in self.fincas:
            activa = " (activa)" if f is self.finca_actual else ""
            print(f"  {f.nombre}{activa}: {len(f.lotes)} lotes, {len(f.familias)} familias")

    # ---------- LOTES ----------
    def registrar_lote(self):
        if not self._requiere_finca():
            return
        nombre = pedir("Nombre del lote: ", tipo=str)
        try:
            self.finca_actual.agregar_lote(Lote(nombre))
            print(f"  Lote '{nombre}' registrado.")
        except ValueError as e:
            print(f"  {e}")

    # ---------- FAMILIAS ----------
    def registrar_familia(self):
        if not self._requiere_finca():
            return
        nombre = pedir("Nombre de la familia: ", tipo=str)
        try:
            self.finca_actual.agregar_familia(Familia(nombre))
            print(f"  Familia '{nombre}' registrada.")
        except ValueError as e:
            print(f"  {e}")

    def agregar_miembro(self):
        if not self._requiere_finca():
            return
        if not self.finca_actual.familias:
            print("  Primero registra una familia.")
            return
        for f in self.finca_actual.familias:
            print(f"  {f.nombre}")
        nombre_fam = pedir("Nombre de la familia: ", tipo=str)
        fam = self.finca_actual.buscar_familia(nombre_fam)
        if not fam:
            print("  Familia no encontrada.")
            return

        nombre = pedir("Nombre del miembro: ", tipo=str)
        indice = pedir("Indice (0.0 a 1.0): ", float, 0.0, 1.0)
        es_joven = pedir_si_no("Es el miembro mas joven? (s/n): ")

        padre = None
        if fam.raiz is not None:
            nombre_padre = pedir(
                "Nombre del padre (vacio si es raiz): ",
                tipo=str,
                permitir_vacio=True,
            )
            if nombre_padre:
                padre = fam.buscar_miembro(nombre_padre)
                if not padre:
                    print("  Padre no encontrado.")
                    return
        try:
            fam.agregar_miembro(nombre, indice, padre, es_joven)
            print(f"  Miembro '{nombre}' agregado.")
        except ValueError as e:
            print(f"  {e}")

    # ---------- CULTIVOS ----------
    def _listar_lotes(self):
        print("  Lotes:")
        for i, l in enumerate(self.finca_actual.lotes, 1):
            print(f"    [{i}] {l.nombre}")

    def agregar_cultivo(self):
        if not self._requiere_finca():
            return
        if not self.finca_actual.lotes:
            print("  Primero registra un lote.")
            return
        self._listar_lotes()
        nombre_lote = pedir("Nombre del lote: ", tipo=str)
        lote = self.finca_actual.buscar_lote(nombre_lote)
        if not lote:
            print("  Lote no encontrado.")
            return

        try:
            tipo = pedir("Tipo (Mora / Tomate / Ornamentales): ", tipo=str)
            cultivo = Cultivo(tipo)
        except ValueError as e:
            print(f"  {e}")
            return

        while True:
            nombre = pedir("  Insumo (o 'fin' para terminar): ", tipo=str)
            if nombre.lower() == "fin":
                break
            valor = pedir(f"  Valor de '{nombre}': ", float, 0)
            try:
                cultivo.agregar_insumo(Insumo(nombre, valor))
                print("  Insumo agregado.")
            except ValueError as e:
                print(f"  {e}")

        try:
            lote.agregar_cultivo(cultivo)
            print(f"  Cultivo '{cultivo.nombre}' agregado al lote '{lote.nombre}'.")
        except ValueError as e:
            print(f"  {e}")

    # ---------- pH ----------
    def registrar_ph(self):
        if not self._requiere_finca():
            return
        if not self.finca_actual.lotes:
            print("  Primero registra un lote.")
            return
        self._listar_lotes()
        nombre_lote = pedir("Nombre del lote: ", tipo=str)
        lote = self.finca_actual.buscar_lote(nombre_lote)
        if not lote:
            print("  Lote no encontrado.")
            return

        entrada = pedir(
            "Muestras de pH separadas por coma (ej: 5.2,5.8,4.9): ",
            tipo=str,
        )
        try:
            muestras = [float(x) for x in entrada.split(",")]
        except ValueError:
            print("  Algun valor no es numerico.")
            return

        agregadas = 0
        for m in muestras:
            try:
                lote.agregar_muestra_ph(m)
                agregadas += 1
            except ValueError:
                print(f"  Muestra {m} descartada.")

        if agregadas == 0:
            print("  Ninguna muestra valida.")
            return

        ph = promedio_ph(lote.muestras_ph)
        print(f"\n  pH promedio del lote '{lote.nombre}': {ph:.2f}")
        self._alertas_ph(lote, ph)

    def _alertas_ph(self, lote, ph):
        if not lote.cultivos:
            if ph < 5.5:
                print("  ALERTA: pH bajo, los nutrientes se bloquean.")
            return
        for cultivo in lote.cultivos:
            rango = cultivo.rango_ph()
            if not rango:
                continue
            minimo, maximo, _ = rango
            gramos = cultivo.dosis_cal(ph)
            if ph < minimo:
                print(
                    f"    {cultivo.nombre}: pH bajo (optimo {minimo}-{maximo}). "
                    f"Aplicar {gramos} g de cal por planta."
                )
            elif ph > maximo:
                print(f"    {cultivo.nombre}: pH alto (optimo {minimo}-{maximo}).")
            else:
                print(f"    {cultivo.nombre}: pH adecuado.")

    # ---------- VISTA ----------
    def ver_estructura(self):
        if not self._requiere_finca():
            return
        print(f"\n{self.finca_actual.nombre}")
        for lote in self.finca_actual.lotes:
            print(f"  |-- Lote: {lote.nombre}")
            if lote.muestras_ph:
                print(f"  |     pH promedio: {promedio_ph(lote.muestras_ph):.2f}")
            if not lote.cultivos:
                print("  |     (sin cultivos)")
            for cultivo in lote.cultivos:
                print(f"  |     |-- Cultivo: {cultivo.nombre}")
                for insumo in cultivo.insumos:
                    print(f"  |     |     |-- {insumo.nombre}: ${insumo.valor:,.0f}")
        print("\n  Familias:")
        for fam in self.finca_actual.familias:
            print(f"    Familia: {fam.nombre}")
            fam.mostrar()

    # ---------- COSTOS ----------
    def calcular_costo(self):
        if not self._requiere_finca():
            return
        total = costo_acumulado_nodo(self.finca_actual)
        print(f"\nCosto acumulado total: ${total:,.0f}")

    # ---------- SIMULACION ----------
    def simular_supervivencia(self):
        capital = pedir("Capital inicial ($): ", float, 0.01)
        precio = pedir("Ingreso mensual por ventas ($): ", float, 0)
        costo = pedir("Costo mensual de insumos ($): ", float, 0)

        if precio == 0 and costo == 0:
            print("  Ingreso y costo son cero: la simulacion no tiene sentido.")
            return
        if precio < costo:
            print(f"  Advertencia: pierde ${costo - precio:,.0f} por mes.")
        elif precio == costo:
            print("  Advertencia: el capital no cambia mes a mes.")

        meses = capital_restante(1, capital, precio, costo)
        if meses >= 24:
            print("\nEl productor se mantiene al menos 24 meses (2 anos).")
        else:
            print(f"\nEl productor agota su capital en el mes {meses}.")

    # ---------- VULNERABILIDAD ----------
    def calcular_vulnerabilidad(self):
        if not self._requiere_finca():
            return
        if not self.finca_actual.familias:
            print("  No hay familias registradas.")
            return
        for fam in self.finca_actual.familias:
            if fam.raiz is None:
                print(f"  {fam.nombre}: sin miembros registrados.")
                continue
            indice = indice_vulnerabilidad_sucesion(fam.raiz)
            nivel = "ALTO" if indice >= 1.5 else "MEDIO" if indice >= 1.0 else "BAJO"
            print(f"  {fam.nombre}: indice {indice:.2f} ({nivel})")

    # ---------- PRECIOS ----------
    def comparar_precios(self):
        print("Formato: producto,almacen,precio. Escribe 'fin' para terminar.\n")
        catalogo = {}
        while True:
            linea = pedir("  > ", tipo=str, permitir_vacio=True)
            if linea.lower() == "fin":
                break
            partes = linea.split(",")
            if len(partes) != 3:
                print("  Se esperan 3 campos (producto,almacen,precio).")
                continue
            producto, almacen, precio_txt = [p.strip() for p in partes]
            if not producto or not almacen:
                print("  Producto o almacen vacios.")
                continue
            try:
                precio = float(precio_txt)
            except ValueError:
                print("  El precio debe ser numerico.")
                continue
            if precio <= 0:
                print("  El precio debe ser mayor que cero.")
                continue
            catalogo.setdefault(producto.lower(), []).append((almacen, precio))

        if not catalogo:
            print("\n  No hay registros validos.")
            return

        resultado = almacen_mas_barato_por_producto(catalogo)
        print("\nComparacion por producto:")
        for producto, (mejor, precio, empates) in resultado.items():
            print(f"  {producto}: mas barato en {mejor} (${precio:,.0f})")
            if len(empates) > 1:
                print(f"    Empate entre: {', '.join(empates)}")

    # ---------- ALERTAS ----------
    def generar_alertas(self):
        if not self._requiere_finca():
            return
        print("\n" + "=" * 55)
        print("   ALERTAS DEL PROTOTIPO SUMAPAZ")
        print("=" * 55)
        total = costo_acumulado_nodo(self.finca_actual)
        print(f"Costo acumulado: ${total:,.0f}")

        if not self.finca_actual.familias:
            print("Sin familias registradas: no aplica el indice sucesoral.")
        for fam in self.finca_actual.familias:
            if fam.raiz:
                indice = indice_vulnerabilidad_sucesion(fam.raiz)
                nivel = "alto" if indice >= 1.5 else "controlado"
                print(f"Familia {fam.nombre}: riesgo {nivel} ({indice:.2f}).")

        for lote in self.finca_actual.lotes:
            if lote.muestras_ph:
                ph = promedio_ph(lote.muestras_ph)
                if ph < 5.5:
                    print(f"Lote {lote.nombre}: pH {ph:.2f}, aplicar cal.")
                    for c in lote.cultivos:
                        gramos = c.dosis_cal(ph)
                        if gramos > 0:
                            print(f"  {c.nombre}: {gramos} g de cal por planta.")