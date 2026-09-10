# Reporte de diseno

## Como manejamos las dos pasadas

Las dos pasadas viven en una sola funcion, `ensamblar`, como dos ciclos
seguidos.

El primer ciclo recorre el archivo linea por linea. De cada linea quita los
comentarios y la parte en palabras. Si la primera palabra no es un mnemonico
conocido, entonces es una etiqueta: se guarda en un diccionario
`etiqueta -> direccion` y se sigue leyendo la misma linea. Cada linea con
mnemonico consume una casilla, y el contador de direcciones avanza de uno en
uno desde el 00. Este ciclo no traduce nada, solo produce la tabla de simbolos
y una lista de instrucciones pendientes, cada una con su direccion y el numero
de linea del archivo.

El segundo ciclo ya tiene la tabla completa, asi que traduce cada instruccion
sin importar si su etiqueta se definio antes o despues. El caso que lo
demuestra es `BRP POS` en `diferencia.asm`: cuando el ensamblador lee esa linea
todavia no ha visto `POS`, pero para el segundo ciclo `POS` ya vale 08 y la
instruccion queda como 808. Con una sola pasada seria imposible.

La traduccion es aritmetica simple: el opcode por 100 mas el operando resuelto.
`INP`, `OUT` y `HLT` no llevan operando y tienen un codigo fijo. `DAT` no es
instruccion, solo escribe su valor en la casilla.

## Otras decisiones

**La memoria es una lista de 100 enteros**, creada con `[0] * 100`. Asi las
casillas sin usar ya quedan en `000` sin logica extra. Como `000` tambien es
`HLT`, un programa que se sale de su codigo se detiene en vez de seguir
ejecutando basura.

**El numero de linea viaja con cada instruccion** desde la primera pasada, para
que los errores de la segunda tambien digan en que linea del archivo esta el
problema y no en que direccion de memoria.

**Los errores usan una excepcion propia**, `ErrorEnsamblador`. El bloque
principal la atrapa e imprime el mensaje, asi el usuario nunca ve un traceback.

**El interprete no se reescribio, se reuso.** Es el de la Sesion 5, con la
funcion `ejecutar_lmc` sin un solo cambio. Lo unico que se movio fue la parte
que lee el archivo y pide las entradas, que ahora vive bajo
`if __name__ == "__main__"` para que el ensamblador pueda importar la funcion
sin que se dispare esa parte.

## Errores encontrados durante el desarrollo

**Distinguir una etiqueta de un mnemonico.** La primera version suponia que si
la linea empezaba sin espacios era una etiqueta, pero eso se rompe en cuanto
alguien indenta distinto. Se cambio por la regla real: si la primera palabra no
esta en la lista de mnemonicos, es una etiqueta. Ahora la indentacion es puro
adorno.

**Etiquetas con distinta capitalizacion.** `BRA fin` no encontraba `FIN`. Se
resolvio normalizando a mayusculas tanto al definir como al usar la etiqueta.

**El mensaje de mnemonico desconocido senalaba la palabra equivocada.** Con
`SUMA 5`, el ensamblador tomaba `SUMA` como etiqueta y luego se quejaba de `5`,
que no ayudaba nada. Ahora el mensaje muestra la linea completa. En el camino
salio un caso peor: una linea con una sola palabra mal escrita se aceptaba como
etiqueta y no daba ningun error. Se corrigio exigiendo que despues de la
etiqueta si venga un mnemonico.

**El limite de 100 casillas.** Al principio se revisaba al final, cuando la
lista de instrucciones ya estaba armada, y el mensaje no podia decir en que
linea se paso. Ahora se revisa mientras se asignan direcciones.

## Extensiones opcionales

Ninguna. El ensamblador soporta solo los once mnemonicos minimos. El interprete
de la Sesion 5 conserva su `CALL` y `RET`, porque era parte de esa sesion, pero
el ensamblador no los emite.
