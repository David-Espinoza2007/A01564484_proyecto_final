"""Interprete del Little Man Computer (LMC).

Es el interprete de la Sesion 5 (`sesion05.py`), reusado tal cual. Ya traia la
extension de subrutinas del ejercicio 4: CALL (opcode 4xx) y RET (999) con una
pila, que es lo que permite llamadas anidadas.

Lo unico que se le agrego para el proyecto son tres protecciones, marcadas con
un comentario, para que un programa mal escrito de un mensaje claro en vez de
un traceback: entradas agotadas, contador de programa fuera de memoria y ciclo
infinito.
"""
import sys


class ErrorEjecucion(Exception):
    """Error detectado mientras corre el programa."""


def _leer(entradas: list) -> int:
    """Agregado para el proyecto: si ya no hay entradas, las pide por teclado."""
    texto = str(entradas.pop(0)) if entradas else input("Entrada: ")
    try:
        return int(texto)
    except ValueError:
        raise ErrorEjecucion(f"entrada invalida: '{texto}' no es un numero")


def ejecutar_lmc(memoria: list, entradas: list, max_pasos: int = 100000) -> list:
    """memoria: lista de 100 enteros de 3 digitos (instrucciones/datos codificados).
    entradas: cola de valores para INP.
    Regresa la lista de valores enviados por OUT."""
    memoria = list(memoria)
    pc = 0
    acumulador = 0
    salidas = []
    entradas = list(entradas)
    pila = []
    pasos = 0

    while True:
        pasos += 1
        if pasos > max_pasos:                 # agregado: corta los ciclos infinitos
            raise ErrorEjecucion(
                f"el programa no termino despues de {max_pasos} pasos (posible ciclo infinito)")
        if not 0 <= pc <= 99:                 # agregado: PC fuera de las 100 casillas
            raise ErrorEjecucion(f"el contador de programa salio de la memoria ({pc})")

        instruccion = memoria[pc]
        opcode = instruccion // 100
        direccion = instruccion % 100
        pc += 1

        if instruccion == 0:                  # HLT
            break

        elif instruccion == 901:              # INP
            acumulador = _leer(entradas)

        elif instruccion == 902:              # OUT
            salidas.append(acumulador)

        elif instruccion == 999:              # RET
            if not pila:                      # agregado: RET sin CALL pendiente
                raise ErrorEjecucion(f"RET en la direccion {pc - 1:02d} sin un CALL pendiente")
            pc = pila.pop()

        elif opcode == 5:                     # LDA
            acumulador = memoria[direccion]

        elif opcode == 3:                     # STA
            memoria[direccion] = acumulador

        elif opcode == 1:                     # ADD: se mantiene el modulo (overflow real de 3 digitos)
            acumulador = (acumulador + memoria[direccion]) % 1000

        elif opcode == 2:                     # SUB: sin modulo, para que el signo quede disponible para BRP
            acumulador = acumulador - memoria[direccion]

        elif opcode == 4:                     # CALL
            pila.append(pc)
            pc = direccion

        elif opcode == 6:                     # BRA
            pc = direccion

        elif opcode == 7:                     # BRZ
            if acumulador == 0:
                pc = direccion

        elif opcode == 8:                     # BRP
            if acumulador >= 0:
                pc = direccion

        else:
            raise ErrorEjecucion(f"Opcode desconocido: {instruccion} en la direccion {pc - 1:02d}")

    return salidas


def cargar(nombre_archivo: str) -> list:
    """Lee un archivo 'direccion,instruccion' y devuelve las 100 casillas."""
    memoria = [0] * 100
    with open(nombre_archivo, encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip():
                direccion, instruccion = linea.strip().split(",")
                memoria[int(direccion)] = int(instruccion)
    return memoria


if __name__ == "__main__":
    # Uso directo, igual que en la Sesion 5: python3 interprete.py programa1.txt
    memoria = cargar(sys.argv[1])
    entradas = [int(v) for v in input("Entradas: ").split()]
    try:
        print(ejecutar_lmc(memoria, entradas))
    except ErrorEjecucion as e:
        print(f"Error de ejecucion: {e}", file=sys.stderr)
        sys.exit(1)
