# Ensamblador de dos pasadas para el LMC

Proyecto final TC1032. Traduce pseudo-ensamblador del LMC a codigo maquina de
3 digitos y lo ejecuta con el interprete de la Sesion 5.

## Como ejecutar

Ensambla el programa, imprime las 100 casillas, pide las entradas y muestra la
salida:

```bash
python3 ensamblador.py programas/suma.asm
```

El interprete tambien se puede correr solo, con un archivo ya ensamblado:

```bash
python3 interprete.py programa1.txt
```

## Formato de entrada

Un mnemonico por linea. La etiqueta, si la hay, va al inicio de la linea. Lo que
sigue a `//` o a `#` es comentario. Las lineas en blanco se ignoran.

```
// suma de dos numeros
        INP
        STA N1
        INP
        ADD N1
        OUT
        HLT
N1      DAT 000
```

Mnemonicos soportados: `INP`, `OUT`, `LDA`, `STA`, `ADD`, `SUB`, `BRA`, `BRZ`,
`BRP`, `HLT` y `DAT`. El operando puede ser una etiqueta o un numero.

## Formato de salida

100 lineas, `direccion,instruccion`. Las casillas sin usar quedan en `000`.

```
00,901
01,306
...
99,000
```

## Programas de prueba y resultados esperados

| Programa | Entradas | Salida esperada |
|---|---|---|
| `programas/suma.asm` | 7 5 | 12 |
| `programas/suma.asm` | 3 9 | 12 |
| `programas/suma.asm` | 50 49 | 99 |
| `programas/diferencia.asm` | 7 5 | 2 |
| `programas/diferencia.asm` | 3 9 | 6 |
| `programas/diferencia.asm` | 99 1 | 98 |
| `programas/mayor.asm` | 7 5 | 7 |
| `programas/mayor.asm` | 3 9 | 9 |
| `programas/mayor.asm` | 4 4 | 4 |

## Errores que se detectan

```
Error de ensamblado: linea 1: mnemonico desconocido en 'SUMA 5'
Error de ensamblado: linea 1: la etiqueta 'FIN' nunca fue definida
Error de ensamblado: linea 2: la etiqueta 'X' ya estaba definida
Error de ensamblado: linea 101: el programa excede las 100 casillas de memoria
```
