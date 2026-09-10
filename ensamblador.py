"""Ensamblador de dos pasadas para el LMC.

Uso: python3 ensamblador.py programa.asm
"""
import sys

from interprete import ejecutar_lmc

CON_OPERANDO = {"ADD": 1, "SUB": 2, "STA": 3, "LDA": 5, "BRA": 6, "BRZ": 7, "BRP": 8}
SIN_OPERANDO = {"HLT": 0, "INP": 901, "OUT": 902}
MNEMONICOS = set(CON_OPERANDO) | set(SIN_OPERANDO) | {"DAT"}


class ErrorEnsamblador(Exception):
    pass


def ensamblar(texto: str) -> list:
    """Traduce el codigo fuente y devuelve las 100 casillas de memoria."""

    # Primera pasada: asigna una direccion a cada instruccion y arma la tabla de etiquetas.
    instrucciones = []
    etiquetas = {}
    direccion = 0
    for nlinea, linea in enumerate(texto.splitlines(), 1):
        tokens = linea.split("//")[0].split("#")[0].split()
        if not tokens:
            continue
        if tokens[0].upper() not in MNEMONICOS:
            etiqueta = tokens.pop(0).upper()
            if etiqueta in etiquetas:
                raise ErrorEnsamblador(f"linea {nlinea}: la etiqueta '{etiqueta}' ya estaba definida")
            etiquetas[etiqueta] = direccion
        if not tokens or tokens[0].upper() not in MNEMONICOS:
            raise ErrorEnsamblador(f"linea {nlinea}: mnemonico desconocido en '{linea.strip()}'")
        if direccion > 99:
            raise ErrorEnsamblador(f"linea {nlinea}: el programa excede las 100 casillas de memoria")
        operando = tokens[1] if len(tokens) > 1 else None
        instrucciones.append((direccion, tokens[0].upper(), operando, nlinea))
        direccion += 1

    # Segunda pasada: traduce cada instruccion con la tabla de etiquetas ya completa.
    memoria = [0] * 100
    for direccion, mnemonico, operando, nlinea in instrucciones:
        if operando is None:
            valor = 0
        elif operando.isdigit():
            valor = int(operando)
        elif operando.upper() in etiquetas:
            valor = etiquetas[operando.upper()]
        else:
            raise ErrorEnsamblador(f"linea {nlinea}: la etiqueta '{operando}' nunca fue definida")

        if mnemonico == "DAT":
            memoria[direccion] = valor
        elif mnemonico in SIN_OPERANDO:
            memoria[direccion] = SIN_OPERANDO[mnemonico]
        else:
            memoria[direccion] = CON_OPERANDO[mnemonico] * 100 + valor
    return memoria


if __name__ == "__main__":
    try:
        archivo = open(sys.argv[1], "r")
        memoria = ensamblar(archivo.read())
        archivo.close()
    except ErrorEnsamblador as error:
        print(f"Error de ensamblado: {error}")
        sys.exit(1)

    for direccion, instruccion in enumerate(memoria):
        print(f"{direccion:02d},{instruccion:03d}")

    entradas = input("Entradas: ").split()
    for i in range(len(entradas)):
        entradas[i] = int(entradas[i])

    print(ejecutar_lmc(memoria, entradas))
