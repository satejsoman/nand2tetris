// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// This program multiplies R0 by R1 by adding R1 to itself R0 times.

    @2      // register for output 
    M=0
    @i      // counter for product
    M=0
(LOOP)
    @i     // load our counter
    D=M
    @0 
    D=D-M  // subtract R1 from the counter
    @END
    D;JGE  // if i - R0 > 0; then we're done

    @1 
    D=M    // load R1
    @2 
    M=D+M  // add R1 to R2
    @i    
    M=M+1  // increment our counter 
    @LOOP
    0;JMP
    

(END)
    @END
    0;JMP // infinite loop to exit 