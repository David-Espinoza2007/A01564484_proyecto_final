// el mayor de dos numeros
// Lee X y Y, si X-Y >= 0 muestra X, si no muestra Y.
        INP
        STA X
        INP
        STA Y
        LDA X
        SUB Y
        BRP XMAYOR
        LDA Y
        OUT
        BRA FIN
XMAYOR  LDA X
        OUT
FIN     HLT
X       DAT 000
Y       DAT 000
