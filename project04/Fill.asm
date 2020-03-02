// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(INIT) // initialize current and max pixel values 
    @SCREEN  // minimum screen pixel value 
    D=A   
    @pixel
    M=D     
    
    // figure out last register value to use as stop condition 
    @24576 // = 16384 + 512*16, aka number of total registers
    D=A
    @maxpixel
    M=D

(MAIN) // main event loop that dispatches on keyboard state
    @KBD 
    D=M    // get current keyboard state
    @BLACK
    D;JEQ  // if nothing pressed, run black-fill routine
    @WHITE
    0;JMP  // else go to white-fill routine

(BLACK) // black-fill routine 
    @pixel // if we're at the max pixel value, do nothing and return to main loop 
    D=M 
    @maxpixel 
    D=D-M 
    @MAIN
    D;JGE

    @pixel // load current pixel pointer
    A=M    // load current pixel value 
    M=-1   // fill register with 1s
    @pixel 
    M=M+1  // increment current pixel pointer
    @MAIN  // go back to main loop to dispatch on new keyboard state
    0;JMP

(WHITE) 
    @pixel // if we're at the min pixel value, do nothing and return to main loop 
    D=M 
    @SCREEN 
    D=D-M 
    @MAIN
    D;JLE

    @pixel // load current pixel pointer
    A=M    // load current pixel value 
    M=0   // fill register with 0s
    @pixel 
    M=M-1  // decrement current pixel pointer
    @MAIN  // go back to main loop to dispatch on new keyboard state
    0;JMP