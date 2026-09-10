"""Pruebas del ensamblador y del interprete. Correr con: python test_ensamblador.py"""
from ensamblador import ensamblar, ErrorEnsamblador
from interprete import ejecutar, ErrorEjecucion


def fuente(nombre):
    with open(f"programas/{nombre}", encoding="utf-8") as f:
        return f.read()


def correr(nombre, entradas):
    return ejecutar(ensamblar(fuente(nombre)), entradas)


def test_traduccion():
    memoria = ensamblar(fuente("suma.asm"))
    assert memoria[:7] == [901, 306, 901, 106, 902, 0, 0], memoria[:7]
    assert memoria[7:] == [0] * 93
    assert len(memoria) == 100


def test_etiqueta_hacia_adelante():
    # BRP POS se resuelve a la direccion 08 aunque POS aparezca despues.
    memoria = ensamblar(fuente("diferencia.asm"))
    assert memoria[:12] == [901, 310, 901, 311, 210, 808, 510, 211, 902, 0, 0, 0], memoria[:12]


def test_ejecucion():
    assert correr("suma.asm", [7, 5]) == [12]
    assert correr("suma.asm", [50, 49]) == [99]
    assert correr("diferencia.asm", [7, 5]) == [2]
    assert correr("diferencia.asm", [3, 9]) == [6]
    assert correr("mayor.asm", [7, 5]) == [7]
    assert correr("mayor.asm", [3, 9]) == [9]
    assert correr("subrutina.asm", [5]) == [20]      # CALL/RET anidados


def test_errores():
    def falla(texto):
        try:
            ensamblar(texto)
        except ErrorEnsamblador as e:
            return str(e)
        raise AssertionError(f"no detecto el error en: {texto!r}")

    assert "desconocido" in falla("        SUMA 5")
    assert "nunca fue definida" in falla("        LDA FALTANTE\n        HLT")
    assert "ya estaba definida" in falla("X       DAT 1\nX       DAT 2")
    assert "100 casillas" in falla("        HLT\n" * 101)


def test_error_ejecucion():
    try:
        ejecutar([903] + [0] * 99)          # RET sin CALL
    except ErrorEjecucion as e:
        assert "sin un CALL" in str(e)
    else:
        raise AssertionError("no detecto el RET sin CALL")


if __name__ == "__main__":
    for nombre, prueba in sorted(globals().items()):
        if nombre.startswith("test_"):
            prueba()
            print(f"ok  {nombre}")
    print("todas las pruebas pasaron")
