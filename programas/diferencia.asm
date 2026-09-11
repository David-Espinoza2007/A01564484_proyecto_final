// diferencia positiva entre dos numeros
// POS se usa en BRP POS antes de estar definida: obliga a las dos pasadas.
        INP
        STA A
        INP
        STA B
        SUB A
        BRP POS
        LDA A
        SUB B
POS     OUT
        HLT
A       DAT 000
B       DAT 000
