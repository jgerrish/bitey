;;;
;;; This program was created to help in finding correct
;;; algorithms for addition and subtraction
;;; It was decompiled from a binary by da65, from the cc65 compiler toolset
;;; by Christian Groessler, dqh, Greg King, groepaz, Oliver Schmidt
;;; and others.
;;; Simply change CLD, SEC and ADC to try other combinations


        .setcpu "6502"

L0010           := $0010
L0021           := $0021
L0033           := $0033
L003E           := $003E
        cld
        nop
        jsr     L0010
        jsr     L0021
        brk
        brk
        brk
        brk
        brk
        brk
        brk
        brk
        lda     #$00
        sta     $00
        lda     #$04
        sta     $81
        ldy     #$FF
LFFD9:  tya
        sta     ($80),y
        dey
        bne     LFFD9
        rts

        ldy     #$00
        ldx     #$00
LFFE4:  txa
        sec
        adc     ($80),y
        jsr     L0033
        inx
        bne     LFFE4
        iny
        bne     LFFE4
        rts

        pha
        jsr     L003E
        php
        pla
        jsr     L003E
        pla
        rts

        sta     $0F
        rts

