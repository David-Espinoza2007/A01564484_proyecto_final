# Reporte de diseno

## Como se manejaron las dos pasadas

El ensamblador esta partido en dos funciones que se pueden leer y probar por
separado: `primera_pasada` y `segunda_pasada`.

La primera pasada recorre el archivo linea por linea. De cada linea quita los
comentarios y la parte en palabras. Si la primera palabra no es un mnemonico
conocido, entonces es una etiqueta: se guarda en un diccionario
`etiqueta -> direccion` y se sigue leyendo la misma linea. Cada linea que si
tiene mnemonico consume una casilla de memoria, y el contador de direcciones
avanza de uno en uno desde el 00. Esta pasada no traduce nada; solo produce la
tabla de simbolos y una lista de instrucciones pendientes, cada una con la
direccion que le toco y el numero de linea del archivo original.

La segunda pasada ya tiene la tabla completa, asi que puede traducir cada
instruccion sin importar si su etiqueta se definio antes o despues. El caso que
lo demuestra es `BRP POS` en `diferencia.asm`: cuando el ensamblador lee esa
linea todavia no ha visto `POS`, pero para la segunda pasada `POS` ya vale 08 y
la instruccion queda como 808. Con una sola pasada habria sido imposible.

La traduccion en si es aritmetica simple: el opcode por 100 mas el operando
resuelto. `INP`, `OUT`, `RET` y `HLT` no llevan operando y tienen un codigo
fijo. `DAT` no es una instruccion, solo escribe su valor en la casilla.

## Decisiones que se tomaron

**Memoria como lista de 100 enteros.** Se crea con `[0] * 100`, asi las
casillas que el programa no usa ya quedan en `000` sin logica extra. Como
`000` tambien es `HLT`, un programa que se sale de su codigo se detiene en vez
de seguir ejecutando basura.

**El numero de linea viaja con cada instruccion.** Se guarda desde la primera
pasada para que los errores de la segunda tambien puedan decir en que linea del
archivo esta el problema, no en que direccion de memoria.

**Una sola excepcion por etapa.** `ErrorEnsamblador` para los errores del
codigo fuente y `ErrorEjecucion` para los de la corrida. La linea de comandos
las atrapa y las imprime como mensaje. El usuario nunca ve un traceback.

**El interprete no se reescribio, se reuso.** Es el de la Sesion 5, con su
funcion `ejecutar_lmc` intacta, incluyendo la extension de subrutinas del
ejercicio 4 de esa sesion: `CALL` con opcode 4xx y `RET` con 999, los dos
codigos que el conjunto LMC del curso dejaba libres. El ensamblador tuvo que
adaptarse a esos codigos, no al reves. Al interprete solo se le agregaron tres
protecciones, cada una marcada con un comentario en el codigo, para que un
programa mal escrito de un mensaje y no un traceback: entradas agotadas,
contador de programa fuera de las 100 casillas y limite de pasos contra ciclos
infinitos.

**El acumulador conserva el signo despues de `SUB`.** Es la decision que ya
venia de la Sesion 5: `ADD` aplica modulo 1000 para simular el desbordamiento
real de tres digitos, pero `SUB` no lo aplica, porque si lo hiciera `BRP`
perderia la informacion del signo y no podria distinguir un resultado negativo.
Por eso `BRP` es simplemente "salta si el acumulador no es negativo".

**Nada mas que la libreria estandar.** El proyecto no necesita ninguna
dependencia externa. `argparse` cubre la linea de comandos y el resto son
diccionarios y listas.

## Errores encontrados durante el desarrollo

**Distinguir una etiqueta de un mnemonico.** La primera version suponia que si
la linea empezaba sin espacios era una etiqueta, pero eso se rompe en cuanto
alguien indenta distinto. Se cambio por la regla real: si la primera palabra no
esta en la lista de mnemonicos, es una etiqueta. Ahora la indentacion es puro
adorno.

**Etiquetas con distinta capitalizacion.** `BRA fin` no encontraba `FIN`. Se
resolvio normalizando a mayusculas tanto al definir como al usar la etiqueta.

**Se habian inventado codigos que no eran los del curso.** La primera version
del ensamblador emitia `903` para `RET`, un codigo elegido al azar. El
interprete de la Sesion 5 usa `999`, que es uno de los dos codigos que el
conjunto LMC del curso deja sin ocupar. El ensamblador quedaba generando
programas que el interprete no entendia. Se corrigio la tabla de opcodes del
ensamblador para que coincida con el interprete, y se agrego una prueba que
compara el ensamblado de `diferencia.asm` contra `programa2.txt` de la Sesion 5:
salen identicos linea por linea.

**Programas que nunca terminan.** Un salto mal puesto dejaba al interprete en
un ciclo infinito. Se le puso un limite de pasos que corta y avisa en vez de
colgarse.

**El limite de 100 casillas.** Al principio se revisaba al final, cuando la
lista de instrucciones ya estaba armada, y el mensaje no podia decir en que
linea se paso. Ahora se revisa mientras se asignan direcciones.

## Extensiones opcionales implementadas

**Subrutinas anidadas con `CALL` (4xx) y `RET` (999).** El interprete de la
Sesion 5 guarda la direccion de retorno en una pila de Python, asi que una
subrutina puede llamar a otra sin limite. Lo que el proyecto agrego fue poder
escribirlas con etiquetas en vez de direcciones numericas: ahora se escribe
`CALL DOBLE` y el ensamblador resuelve la direccion.
`programas/subrutina.asm` lo ejercita, con `CUAD` llamando dos veces a `DOBLE`
para multiplicar por cuatro. Si aparece un `RET` sin `CALL` pendiente, se
reporta el error con su direccion.

**Linea de comandos.** `python3 ensamblador.py programa.asm --run --input 7,5`
ensambla y corre en un solo paso. Tambien acepta `-o` para guardar el ensamblado
en un archivo, y si no se dan entradas las pide por teclado.

**Pruebas automaticas.** `test_ensamblador.py` compara el ensamblado contra los
codigos esperados de los programas de ejemplo, corre los cuatro programas con
varias entradas, comprueba que los cuatro errores obligatorios se detecten y
verifica que el archivo que produce el ensamblador se pueda releer con el
cargador de la Sesion 5. Corre con `python3 test_ensamblador.py` y no necesita
ninguna libreria de pruebas.
