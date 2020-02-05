/* This is a multiline comment
spanning multiple lines */

(KBDLOOP)
    @KBD    // loop until key pressed
    D=M
    @KBDLOOP
    D;JEQ

    @50     // setup 
    D=A 
    @R0 
