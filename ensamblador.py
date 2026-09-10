"""Ensamblador de dos pasadas para el Little Man Computer (LMC).

Uso:
    python ensamblador.py programas/suma.asm
    python ensamblador.py programas/suma.asm --run --input 7,5
    python ensamblador.py programas/suma.asm -o salida.txt
"""
import argparse
import sys

from interprete import ejecutar_lmc, ErrorEjecucion

CON_OPERANDO = {"ADD": 1, "SUB": 2, "STA": 3, "CALL": 4, "LDA": 5, "BRA": 6, "BRZ": 7, "BRP": 8}
SIN_OPERANDO = {"HLT": 0, "INP": 901, "OUT": 902, "RET": 999}
MNEMONICOS = set(CON_OPERANDO) | set(SIN_OPERANDO) | {"DAT"}


class ErrorEnsamblador(Exception):
    """Error en el programa fuente, se reporta con mensaje claro."""


def _tokens(linea):
    """Quita comentarios (// o #) y parte la linea en palabras."""
    for marca in ("//", "#"):
        linea = linea.split(marca)[0]
    return linea.split()


def primera_pasada(texto):
    """Asigna una direccion a cada instruccion y arma la tabla de simbolos.

    Devuelve (instrucciones, etiquetas), donde cada instruccion es
    (direccion, mnemonico, operando, numero_de_linea).
    """
    instrucciones = []
    etiquetas = {}
    direccion = 0
    for nlinea, linea in enumerate(texto.splitlines(), 1):
        tokens = _tokens(linea)
        if not tokens:
            continue
        if tokens[0].upper() not in MNEMONICOS:          # la primera palabra es una etiqueta
            etiqueta = tokens.pop(0).upper()
            if etiqueta in etiquetas:
                raise ErrorEnsamblador(
                    f"linea {nlinea}: la etiqueta '{etiqueta}' ya estaba definida "
                    f"en la direccion {etiquetas[etiqueta]:02d}")
            etiquetas[etiqueta] = direccion
            if not tokens:                               # etiqueta sola, no ocupa casilla
                continue
        mnemonico = tokens[0].upper()
        if mnemonico not in MNEMONICOS:
            raise ErrorEnsamblador(f"linea {nlinea}: mnemonico desconocido '{tokens[0]}'")
        if direccion > 99:
            raise ErrorEnsamblador(
                f"linea {nlinea}: el programa excede las 100 casillas de memoria (00-99)")
        operando = tokens[1] if len(tokens) > 1 else None
        instrucciones.append((direccion, mnemonico, operando, nlinea))
        direccion += 1
    return instrucciones, etiquetas


def _valor(operando, etiquetas, nlinea, maximo):
    """Resuelve un operando: numero literal o etiqueta de la tabla de simbolos."""
    if operando is None:
        return 0
    if operando.lstrip("+-").isdigit():
        numero = int(operando)
    elif operando.upper() in etiquetas:
        numero = etiquetas[operando.upper()]
    else:
        raise ErrorEnsamblador(f"linea {nlinea}: la etiqueta '{operando}' nunca fue definida")
    if not 0 <= numero <= maximo:
        raise ErrorEnsamblador(f"linea {nlinea}: el valor {numero} esta fuera del rango 0-{maximo}")
    return numero


def segunda_pasada(instrucciones, etiquetas):
    """Traduce cada instruccion a su codigo de 3 digitos y llena las 100 casillas."""
    memoria = [0] * 100
    for direccion, mnemonico, operando, nlinea in instrucciones:
        if mnemonico == "DAT":
            memoria[direccion] = _valor(operando, etiquetas, nlinea, 999)
        elif mnemonico in SIN_OPERANDO:
            if operando is not None:
                raise ErrorEnsamblador(f"linea {nlinea}: '{mnemonico}' no lleva operando")
            memoria[direccion] = SIN_OPERANDO[mnemonico]
        else:
            if operando is None:
                raise ErrorEnsamblador(f"linea {nlinea}: '{mnemonico}' necesita un operando")
            memoria[direccion] = CON_OPERANDO[mnemonico] * 100 + _valor(operando, etiquetas, nlinea, 99)
    return memoria


def ensamblar(texto):
    """Ensambla el codigo fuente y devuelve las 100 casillas de memoria."""
    instrucciones, etiquetas = primera_pasada(texto)
    return segunda_pasada(instrucciones, etiquetas)


def formato(memoria):
    """Las 100 casillas como texto 'direccion,instruccion'."""
    return "\n".join(f"{d:02d},{c:03d}" for d, c in enumerate(memoria))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ensamblador de dos pasadas para el LMC")
    parser.add_argument("archivo", help="programa fuente en pseudo-ensamblador (.asm)")
    parser.add_argument("-o", "--salida", help="archivo donde guardar las 100 casillas")
    parser.add_argument("--run", action="store_true", help="ejecutar el programa ensamblado")
    parser.add_argument("--input", default="", help="entradas para INP separadas por coma, ej: 7,5")
    args = parser.parse_args(argv)

    try:
        with open(args.archivo, encoding="utf-8") as f:
            memoria = ensamblar(f.read())
    except OSError as e:
        print(f"Error: no se pudo leer '{args.archivo}': {e.strerror}", file=sys.stderr)
        return 1
    except ErrorEnsamblador as e:
        print(f"Error de ensamblado en {args.archivo}, {e}", file=sys.stderr)
        return 1

    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as f:
            f.write(formato(memoria) + "\n")
        print(f"Ensamblado guardado en {args.salida}")

    if args.run:
        entradas = [v for v in args.input.split(",") if v.strip()]
        try:
            for valor in ejecutar_lmc(memoria, entradas):
                print(valor)
        except ErrorEjecucion as e:
            print(f"Error de ejecucion: {e}", file=sys.stderr)
            return 1
    elif not args.salida:
        print(formato(memoria))
    return 0


if __name__ == "__main__":
    sys.exit(main())
