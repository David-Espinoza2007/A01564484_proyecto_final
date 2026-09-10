# Ensamblador de dos pasadas para el LMC

Proyecto final de TC1032. Traduce pseudo-ensamblador del Little Man Computer
(mnemonicos + etiquetas) a codigo maquina de 3 digitos y lo ejecuta en un
interprete LMC.

Solo usa la libreria estandar de Python 3. No hay que instalar nada.

## Archivos

| Archivo | Que hace |
|---|---|
| `ensamblador.py` | Las dos pasadas, la tabla de simbolos y la linea de comandos |
| `interprete.py` | Ejecuta las 100 casillas de memoria |
| `test_ensamblador.py` | Pruebas automaticas de todo lo anterior |
| `programas/*.asm` | Programas de prueba |
| `REPORTE.md` | Decisiones de diseno y problemas encontrados |

## Como se usa

Ensamblar e imprimir las 100 casillas:

```bash
python3 ensamblador.py programas/suma.asm
```

Ensamblar y ejecutar con entradas ya dadas:

```bash
python3 ensamblador.py programas/suma.asm --run --input 7,5
```

Guardar el ensamblado en un archivo:

```bash
python3 ensamblador.py programas/mayor.asm -o salida.txt
```

Si se usa `--run` sin `--input`, el programa pide cada valor por teclado
cuando encuentra un `INP`.

Correr las pruebas:

```bash
python3 test_ensamblador.py
```

## Formato de entrada

Un mnemonico por linea. La etiqueta, si la hay, va al principio de la linea.
Todo lo que sigue a `//` o a `#` es comentario. Las lineas en blanco se ignoran.

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

El operando puede ser una etiqueta o un numero. Las etiquetas no distinguen
mayusculas de minusculas.

## Formato de salida

100 lineas, una por casilla, con la direccion y la instruccion. Las casillas
que el programa no usa quedan en `000`.

```
00,901
01,306
...
99,000
```

## Mnemonicos

| Mnemonico | Codigo | Que hace |
|---|---|---|
| `ADD x` | 1xx | Suma al acumulador el contenido de la casilla x |
| `SUB x` | 2xx | Le resta al acumulador el contenido de la casilla x |
| `STA x` | 3xx | Guarda el acumulador en la casilla x |
| `CALL x` | 4xx | Llama a la subrutina que empieza en x (extension opcional) |
| `LDA x` | 5xx | Carga en el acumulador el contenido de la casilla x |
| `BRA x` | 6xx | Salta a x |
| `BRZ x` | 7xx | Salta a x si el acumulador es cero |
| `BRP x` | 8xx | Salta a x si el acumulador no es negativo |
| `INP` | 901 | Lee un valor y lo pone en el acumulador |
| `OUT` | 902 | Imprime el acumulador |
| `RET` | 903 | Regresa de la subrutina (extension opcional) |
| `HLT` | 000 | Termina el programa |
| `DAT n` | nnn | Reserva una casilla con el valor n (0 por omision) |

## Programas de prueba y resultados esperados

| Programa | Entradas | Salida esperada |
|---|---|---|
| `suma.asm` | 7,5 | 12 |
| `suma.asm` | 3,9 | 12 |
| `suma.asm` | 0,0 | 0 |
| `suma.asm` | 50,49 | 99 |
| `diferencia.asm` | 7,5 | 2 |
| `diferencia.asm` | 3,9 | 6 |
| `diferencia.asm` | 5,5 | 0 |
| `diferencia.asm` | 99,1 | 98 |
| `mayor.asm` | 7,5 | 7 |
| `mayor.asm` | 3,9 | 9 |
| `mayor.asm` | 4,4 | 4 |
| `subrutina.asm` | 5 | 20 |
| `subrutina.asm` | 2 | 8 |

## Errores que se detectan

Todos salen como un mensaje con el numero de linea, nunca como un traceback:

```
Error de ensamblado en programa.asm, linea 3: mnemonico desconocido 'SUMA'
Error de ensamblado en programa.asm, linea 5: la etiqueta 'FIN' nunca fue definida
Error de ensamblado en programa.asm, linea 9: la etiqueta 'X' ya estaba definida en la direccion 07
Error de ensamblado en programa.asm, linea 101: el programa excede las 100 casillas de memoria (00-99)
```
