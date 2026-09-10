import sys


def ejecutar_lmc(memoria: list, entradas: list) -> list:
    memoria = list(memoria)
    pc = 0
    acumulador = 0
    salidas = []
    entradas = list(entradas)
    pila = []

    while True:
        instruccion = memoria[pc]
        opcode = instruccion // 100
        direccion = instruccion % 100
        pc += 1

        if instruccion == 0:                  # HLT
            break

        elif instruccion == 901:              # INP
            acumulador = entradas.pop(0)

        elif instruccion == 902:              # OUT
            salidas.append(acumulador)

        elif instruccion == 999:              # RET
            pc = pila.pop()

        elif opcode == 5:                     # LDA
            acumulador = memoria[direccion]

        elif opcode == 3:                     # STA
            memoria[direccion] = acumulador

        elif opcode == 1:                     # ADD
            acumulador = (acumulador + memoria[direccion]) % 1000

        elif opcode == 2:                     # SUB
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
            raise ValueError(f"Opcode desconocido: {instruccion}")

    return salidas


if __name__ == "__main__":
    archivo = open(sys.argv[1], "r")

    memoria = [0] * 100

    for linea in archivo:
        direccion, instruccion = linea.strip().split(",")
        memoria[int(direccion)] = int(instruccion)

    archivo.close()

    entradas = input("Entradas: ").split()

    for i in range(len(entradas)):
        entradas[i] = int(entradas[i])

    print(ejecutar_lmc(memoria, entradas))
