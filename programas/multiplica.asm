// Multiplica dos numeros sumando A veces B
        INP
        STA A
        INP
        STA B
CICLO   LDA B
        BRZ FIN
        LDA RES
        ADD A
        STA RES
        LDA B
        SUB UNO
        STA B
        BRA CICLO
FIN     LDA RES
        OUT
        HLT
A       DAT 000
B       DAT 000
RES     DAT 000
UNO     DAT 001