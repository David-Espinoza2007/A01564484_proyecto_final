// subrutina.asm - extension opcional CALL / RET con llamadas anidadas
// Lee N y muestra N*4: CUAD llama dos veces a DOBLE (una llamada dentro de otra).
        INP
        STA N
        CALL CUAD
        LDA N
        OUT
        HLT
CUAD    CALL DOBLE
        CALL DOBLE
        RET
DOBLE   LDA N
        ADD N
        STA N
        RET
N       DAT 000
