"""Interprete del Little Man Computer (LMC).

Ejecuta las 100 casillas de memoria que produce el ensamblador.
Incluye la extension de subrutinas: CALL (4xx) y RET (903), con una pila
que permite llamadas anidadas.
"""


class ErrorEjecucion(Exception):
    """Error detectado mientras corre el programa."""


def _leer(entradas):
    texto = str(entradas.pop(0)) if entradas else input("entrada> ")
    try:
        return int(texto)
    except ValueError:
        raise ErrorEjecucion(f"entrada invalida: '{texto}' no es un numero")


def ejecutar(memoria, entradas=(), max_pasos=100000):
    """Corre el programa y devuelve la lista de valores que imprimio OUT."""
    memoria = list(memoria)
    entradas = list(entradas)
    acumulador = 0
    contador = 0          # program counter: direccion de la siguiente instruccion
    salidas = []
    pila = []             # direcciones de retorno de CALL

    for _ in range(max_pasos):
        if not 0 <= contador <= 99:
            raise ErrorEjecucion(f"el contador de programa salio de la memoria ({contador})")
        instruccion = memoria[contador]
        direccion_actual = contador
        contador += 1
        codigo, dato = divmod(instruccion, 100)

        if instruccion == 0:                      # HLT
            return salidas
        elif codigo == 1:                         # ADD
            acumulador += memoria[dato]
        elif codigo == 2:                         # SUB
            acumulador -= memoria[dato]
        elif codigo == 3:                         # STA
            memoria[dato] = acumulador % 1000
        elif codigo == 4:                         # CALL
            pila.append(contador)
            contador = dato
        elif codigo == 5:                         # LDA
            acumulador = memoria[dato]
        elif codigo == 6:                         # BRA
            contador = dato
        elif codigo == 7:                         # BRZ
            if acumulador == 0:
                contador = dato
        elif codigo == 8:                         # BRP
            if acumulador >= 0:
                contador = dato
        elif instruccion == 901:                  # INP
            acumulador = _leer(entradas)
        elif instruccion == 902:                  # OUT
            salidas.append(acumulador % 1000)
        elif instruccion == 903:                  # RET
            if not pila:
                raise ErrorEjecucion(f"RET en la direccion {direccion_actual:02d} sin un CALL pendiente")
            contador = pila.pop()
        else:
            raise ErrorEjecucion(
                f"instruccion desconocida {instruccion:03d} en la direccion {direccion_actual:02d}")

    raise ErrorEjecucion(f"el programa no termino despues de {max_pasos} pasos (posible ciclo infinito)")
