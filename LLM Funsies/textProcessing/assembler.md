Computer Systems and Professional Practice Professor Matthew Leeke School of Computer Science University of Birmingham Topic 4 - Assembler 


![](images/assembler/Slide_1_Image_1.png)


Session Outline 

Microprocessor Fundamentals Register Transfer Language Assembly Language Subroutines and Stacks Addressing Modes 

**2 Computer Systems and Professional Practice - Assembler** 

## Microprocessor Fundamentals 


![](images/assembler/Slide_3_Image_1.png)


Central Processing Unit (CPU) 

Controls and performs instructions 

Modern CPUs commonly housed on a silicon chip known as a microprocessor 

Microprocessor CPU implementations dominate alternatives 

CPUs are incredibly complex in their implementation but are usually viewed as having two key components 

**Arithmetic Logic Unit (ALU)** - Performs mathematical and logical operations 

**Control Unit (CU)** - Decodes program instructions and handles logistics for the execution of decoded instructions 


![](images/assembler/Slide_4_Image_7.png)

> **[Visual Context: Slide_4_Image_7.png]**
> **Category:** Computer Systems Lecture
> **Core Concept:** Core i9
> **Structural Elements:** Intel logo, Text: CORE i9, Text: X-series
> **Pedagogical Value:** This image is from a computer systems lecture, focusing on core technology and architecture.



**4 Computer Systems and Professional Practice - Assembler** 

## Fundamentals of CPU Operation 

CPU continuously performs instruction cycle 

Computational instructions are retrieved from memory, decoded to form recognisable operations and executed to impact the current state of a CPU 

Commonly known as the fetch-execute cycle or the fetch-decode-execute cycle Instruction cycle takes place over several CPU clock cycles 

Recall the significance of clocks in sequential logic circuits 

Fetch-decode-execute cycle relies on interaction of several CPU components, including ALU and CU 

**5 Computer Systems and Professional Practice - Assembler** 

Fetch-Decode-Execute Components 

**Arithmetic Logic Unit (ALU)** - Performs mathematical and logical operations **Control Unit (CU)** - Decodes program instructions and handles logistics for the execution of decoded instructions 

**Program Counter (PC)** - Tracks the memory address of the next instruction to be executed **Instruction Register (IR)** - Contains most recent instruction fetched 

**Memory Address Register (MAR)** - Contains address of the region of memory to be read or written, i.e., location of data to be accessed 

**Memory Data Register (MDR)** - Contains data fetched from memory or data ready to be written to memory 

**6 Computer Systems and Professional Practice - Assembler** 

## Fetch-Decode-Execute Cycle 

The specifics of an instruction cycle will vary with microprocessor may vary 

**Fetch** 

- Instruction retrieved from memory location held by PC 

- Retrieved instruction stored in IR 

- PC incremented to point to next instruction in memory 

**Decode** 

- Retrieved instruction / operation code / opcode decoded 

- Read effective address to establish opcode type **Execute** 

- CU signals functional CPU components 

- May result in changes to data registers, PC, ALU, I/O, etc... 

**7** 

**Computer Systems and Professional Practice - Assembler** 

I’m Confused... Where’s the Assembler? 

Understanding something about microprocessor operation and their instruction cycles provides an ideal context for us to appreciate programming in an assembly language 

We will revisit many of these issues in subsequent topics 

Of course, we can’t just start writing assembler without some idea of what we can and can’t do 

**How can we think about programming in assembly?** 

**8 Computer Systems and Professional Practice - Assembler** 

## A Worked Example - The 68008 Architecture 

To appreciate the general, we will consider a specific example with common characteristics 

## **Data Registers** 


![](images/assembler/Slide_9_Image_3.png)


**----- Start of picture text -----**<br>
Address Registers<br>**----- End of picture text -----**<br>



![](images/assembler/Slide_9_Image_4.png)

> **[Visual Context: Slide_9_Image_4.png]**
> **Category:** Assembly Language
> **Core Concept:** Program Counter
> **Structural Elements:** Grid 9x9, Stack Pointer
> **Logic:** Stack Pointer points to Program Counter at 32 bits, following 8, 16, and 32 bit operations as shown.
> **Pedagogical Value:** This image visualizes a program counter and stack pointer, fundamental concepts in computer systems and assembly programming.



**----- Start of picture text -----**<br>
A0<br>D0<br>A1<br>D1<br>A2<br>D2<br>A3<br>D3<br>A4<br>D4<br>A5<br>D5<br>A6<br>D6<br>D7 A7 (Stack Pointer)<br>32 bits<br>8 bits<br>16 bits<br>32 bits Program Counter<br>CCR<br>**----- End of picture text -----**<br>


**9 Computer Systems and Professional Practice - Assembler** 

## Programmer’s Model of 68008 CPU 

The programmer's model is a commonly used abstraction, invariably used by assembler programmers, of the internal architecture of a processor 

68008 processor has identical instruction set to the 68000 processor, but has smaller external buses 

Internal registers are 32-bits wide 

Internal data buses are 16-bits wide 

68008 has an 8-bit external data bus (16-bit on 68000) 

68008 has 20-bit external address bus (24-bit for 68000) 

**10 Computer Systems and Professional Practice - Assembler** 

## A 68008 Programmer’s Model 

## Understanding available registers is the cornerstone of a useful programmer’s model 

**Data Registers** 

**Address Registers** 


![](images/assembler/Slide_11_Image_4.png)


**----- Start of picture text -----**<br>
A0<br>D0<br>A1<br>D1<br>A2<br>D2<br>A3<br>D3<br>A4<br>D4<br>A5<br>D5<br>A6<br>D6<br>D7 A7 (Stack Pointer)<br>32 bits<br>8 bits<br>16 bits<br>32 bits Program Counter<br>CCR<br>**----- End of picture text -----**<br>


**11 Computer Systems and Professional Practice - Assembler** 

## Data Registers 

D0 - D7, 32 bit registers, store frequently used values / intermediate results 

ON CHIP 

Strictly speaking we would only need one register on chip - the advantage of many data registers is that fewer references to external memory are required Registers can be treated as long, word or byte 

Long  - 32-bits 

Word - 16-bits  (lowest 16 bits) 

Byte   - 8-bits  (lowest 8 bits) 

**12 Computer Systems and Professional Practice - Assembler** 

## Status Register 

16 bit - Consists of two 8-bit registers 

Various status bits that are set or reset upon certain conditions arising in the arithmetic and logic unit (ALU) 


![](images/assembler/Slide_13_Image_3.png)

> **[Visual Context: Slide_13_Image_3.png]**
> **Category:** Constraint Graph
> **Core Concept:** Domain size calculation
> **Structural Elements:** Grid 9x9
> **Logic:** X N V C (Extend, Negative, Zero, Overflow, Carry)
> **Pedagogical Value:** N/A



**13 Computer Systems and Professional Practice - Assembler** 

Address Registers 

A0 - A6 Used as POINTER REGISTERS in the calculation of operand addresses 

A7 - Additionally used by the processor as a system stack pointer to hold subroutine return addresses etc... 

Operations on addresses do not alter status register Condition Code Register (CCR) 

ALU has capacity to incur changes in status 

**14 Computer Systems and Professional Practice - Assembler** 

## A0-A7, Memory and Stack 

The diagram below illustrates the relationship between address registers, external memory, i.e., not data registers, and the stack **External Memory** 

**External Memory** 


![](images/assembler/Slide_15_Image_3.png)

> **[Visual Context: Slide_15_Image_3.png]**
> **Category:** Constraint Graph
> **Core Concept:** Domain size calculation
> **Structural Elements:** FF00, FF01, FF02, FF03
> **Logic:** FF00 connects to A0, A1, and A7, connecting to FF00, FF01, and FF02 respectively.
> **Pedagogical Value:** None



**----- Start of picture text -----**<br>
  0000  02<br>0001 62<br>0002 22<br>FEFF 45<br>FF00 05<br>A0 FF00<br>FF01 00<br>A1 0001<br>FF02 00<br>FF03 30<br>55<br>A7<br>FF03<br>FFFE<br>FFFF 32<br>stack<br>**----- End of picture text -----**<br>


**15 Computer Systems and Professional Practice - Assembler** 

## Stack Pointer 

A7 - The stack pointer is used as a pointer into an area of memory called the system stack. 

Points to the next free location 

The stack is a Last In First Out (LIFO) structure 

The stack provides temporary storage of essential processor state, e.g., return addresses and registers, during subroutine calls and interrupts 

You will meet this use of the stack again in many different contexts 

A0-A6 may also used by programmer as stack pointers for temporary storage of registers, e.g., arithmetic calculations 

**16 Computer Systems and Professional Practice - Assembler** 

# Program Counter (PC) 

# A 32-bit register that  keeps track of the address at which the next instruction will be found 

In simple terms, it points to the next instruction in memory 

When the current instruction has been read, the PC is incremented to point to the next instruction 

**17 Computer Systems and Professional Practice - Assembler** 

## 68008 Internal Architecture 


![](images/assembler/Slide_18_Image_1.png)


**----- Start of picture text -----**<br>
Address  Data<br>MAR<br>Bus Bus<br>MBR<br>PC<br>External<br>Memory<br>D0<br>A0<br>D1<br>A1<br>D2<br>A2<br>D3<br>A3<br>D4<br>A4<br>Control<br>D5<br>A5<br>Unit<br>D6<br>A6<br>D7<br>A7<br>IR<br>ALU2<br>ALU1<br>CCR<br>MAR - Memory Address Register   MBR - Memory Buffer Register<br>CCR - Condition Code Register  IR - Instruction Register<br>**----- End of picture text -----**<br>


**18 Computer Systems and Professional Practice - Assembler** 

Register Transfer Language 


![](images/assembler/Slide_19_Image_1.png)


## Register Transfer Language 

Used to describe the operations of a microprocessor as it is executing instructions 

← For example, [MAR] [PC] means transfer contents of Program Counter to the Memory Address Register. 

Computer's memory is called Main Store (MS) 

The contents of memory location 12345 is written [ MS(12345) ] 

Try not to confuse register transfer language with assembler instructions 

**20 Computer Systems and Professional Practice - Assembler** 

## Instruction Cycle 

We know quite a bit about the instruction cycle and the components involved in the process To highlight the power of RTL we can use it represent stages of the instruction cycle The RTL representation we will see makes no attempt to account for the pipelining of instructions Pipelining is a common and simple method of speeding up the fetch-execute cycle - you might like to research pipelining in you own time 

**DECODE** 

**START FETCH EXECUTE** 

**21 Computer Systems and Professional Practice - Assembler** 

## RTL - Instruction Fetching in Words 

1. Contents of Program Counter transferred to MAR address buffers and the Program Counter is incremented 

2. MBR loaded from external memory (R/W line set to Read) 

3. Opcode transferred to Instruction Register from MBR 

4. Instruction is decoded 

**22 Computer Systems and Professional Practice - Assembler** 

RTL - Instruction Fetching 

We can represent the fetch stage of the fetch-execute cycle in RTL 

← 1. [MAR] [PC] 

← 2. [PC] [PC] +1 

← 3. [MBR] [MS([MAR])]     (R/W set to Read) 

← 4. [IR] [MBR] 

← 5. CU [IR(opcode)] 

This part of the cycle is the same for each instruction 

**Computer Systems and Professional Practice - Assembler** 

**23** 

## RTL - Fetch and Execute 

We can represent complex actions, such as adding a constant byte to D0 

← 1. [MAR] [PC] 

← 2. [PC] [PC] +1 

← 3. [MBR] [MS([MAR])]           (R/W set to Read) 

← 4. [IR] [MBR] 

← 5. CU [IR(opcode)] 

… 

**Computer Systems and Professional Practice - Assembler** 

**24** 

## RTL - Fetch and Execute 

… 

← 6. [MAR] [PC] 

← 7. [PC] [PC] +1 

← 8. [MBR] [MS([MAR])] 

← 9. ALU [MBR] + D0 

← 10. [D0] ALU 

**Computer Systems and Professional Practice - Assembler** 

**25** 

Assembly Language 


![](images/assembler/Slide_26_Image_1.png)


# C Programming 

You can work at the hardware-software interface by using the C programming language 

C is compiled to assembler - the low level instruction set of the microprocessor Assembler programs are assembled in order to generate loadable binary 

We concentrate on understanding the instruction set 

**27 Computer Systems and Professional Practice - Assembler** 

## Compiler, Assembler and Microprocessor 

## **High-level language (C) program** 

## **Compiler** 

## **Low-level assembler language program** 

**Assembler** 

## **Machine code (binary) program** 

## **Microprocessor** 

**28 Computer Systems and Professional Practice - Assembler** 

# Assembly Language 

Rather than programming in machine code, i.e., placing numbers in memory locations, we prefer to program at a slightly higher level, i.e., in an assembler language 

Assembler language uses easily remembered mnemonics for each instruction, e.g., MOVE D0, D1 

Assembler language also allows memory locations and constants to be given symbolic names A point in a program can be referred to by its name rather than a numeric address 

**29 Computer Systems and Professional Practice - Assembler** 

Machine and Assembler Codes 

Microprocessors "understand" programs of 0's and 1's 

For example: 

**1010 1001 A9 0000 0101 05** Hex is an aid, but what does the following small program do? **D8 A2 FF 9A 18 A9 05 69 07 8D 11 00** 

This is why we use assembly languages 

**30 Computer Systems and Professional Practice - Assembler** 

## Assembler Format 

Assembly languages vary but typically have a similar format: 

**<LABEL>:   <OPCODE>   <OPERAND(S)>     | COMMENT** 

For example: 

**START:  move.b #5, D0 | load D0 | with 5** 

**31** 

**Computer Systems and Professional Practice - Assembler** 

## Example Assembler Program 

Understanding assembler programs is about recognising each small operation and how it fits as part of a larger sequence of operations 

**ORG $4B0 | this program starts at hex 4B0 move.b #5, D0 | load D0 with 5 add.b #$A, D0 | add 10 to D0 move.b D0, ANS | store result in ANS | ANS: DS.B 1 | leave 1 byte of memory empty** 

**| and give it the name ANS** 

**Numbers:** 

**# :** indicates a constant. A number 

without # prefix is an address 

Default number base is DECIMAL 

**$ :** means in HEX **% :** means in BINARY 

**Assembler Directives:** 

**ANS:** A label, i.e., a symbolic name, that must be 

terminated by a colon 

**DS (Define Storage):** instructs the assembler to 

reserve some memory 

**ORG (Origin):** tells the assembler where in memory to start putting the instructions or data 

**32 Computer Systems and Professional Practice - Assembler** 

## 68008 Instruction Set 

There are two aspects to the 68008 instruction set: 

**Instructions** - The commands that tell the processor what operations to perform 

**Addressing Modes** - The ways in which the processor can access data or memory locations, i.e., the ways in which addresses may be calculated by the CPU 

**33 Computer Systems and Professional Practice - Assembler** 

## 68008 Instructions 

The 68008 instruction set is made up of five categories of instructions: 

1. Data Movement 

2. Arithmetic 

3. Logical 

4. Branch 

5. System Control 

We will look briefly at the first four groups 

**34 Computer Systems and Professional Practice - Assembler** 

## Form of 68008 Assembler Instructions 

Assembler instructions are written in the form: 

## **operation.datatype    source,     destination** 

The operation can be on one of three data types: 

**byte** 

**.b (8 bits)** 

**word** 

**.w (2 bytes)** 

**long word** 

**.l (4 bytes)** 

The data type and dot may be omitted if the data type is word 

**35 Computer Systems and Professional Practice - Assembler** 

## 1. Data Movement Instructions 

**move.b** 

**D0, D1** 

**moveb D0, D1** 

**move.w move** 

**D0, D1** 

**D0, D1** 

**move.l $F20, D3** 

**exg.b D4, D5** 

**swap** 

**D2** 

**lea $F20, A3** 

**← | [D1(0:7)] [D0(0:7)]** 

**| the same** 

**← | [D1(0:15)] [D0(0:15)]** 

**| the same** 

**← | [D3(24:31)] [MS($F20)]** 

**← | [D3(16:23)] [MS($F21)]** 

**← | [D3( 8:15)] [MS($F22)]** 

**← | [D3( 0:7)] [MS($F23)]** 

**| (Big-Endian mean this way around)** 

**| exchange** 

**| swap lower and upper words** 

**← | load effective address [A3] [$F20]** 

**36 Computer Systems and Professional Practice - Assembler** 

## 2. Arithmetic Instructions 

The 68008 does not have hardware floating point support – instructions operate on integers 

**add.l  Di, Dj addx.w sub.b Di, Dj subx.b Di, Dj mulu.w** 

**Di, Dj** 

**Di, Dj** 

**muls.w Di, Dj divu.b Di, Dj divs.l  Di, Dj** 

**← | [Dj] [Di] + [Dj] | also add in x bit from CCR** 

**← | [Dj] [Dj] - [Di]** 

**| also subtract x bit from CCR** 

**| unsigned multiplication:** 

**← | [Dj(0:31)] [Di(0:15)] * [Dj(0:15)]** 

**| signed multiplication** 

**37 Computer Systems and Professional Practice - Assembler** 

## 3. Logical Instructions 

These instructions perform bit-wise operations on data and include AND,  OR,  EOR,  NOT 

For example, if register D3 contains 1010 0101, then... 

**AND.B    #%11110000, D3** 

... will produce the result 1010 0000 in the least significant byte of register D3 

**38 Computer Systems and Professional Practice - Assembler** 

## Examples of Logical Instructions - Logic 

Once you understand a few of these operations the operation of the rest becomes much clearer 

**Logical AND:** 1 1 0 1 D0 **AND.B    #$7F, D0** 0 1 1 1 7F D0 0 1 0 1 **(keep just the lower 7 bits and ignore the MSB)** 

1 1 0 1 1 0 1 0 D0 

0 1 1 1 1 1 1 1 7F 

0 1 0 1 1 0 1 0 

**Logical OR: OR.B    D1, D0** 

1 0 0 0 0 0 1 0 D1 

0 0 0 1 0 1 1 0 D0 

D0 1 0 0 1 0 1 1 0 

**39 Computer Systems and Professional Practice - Assembler** 

Examples of Logical Instructions - Shifts 

Shift operations are often fundamental to many computational tasks- remember we achieved multiplication by 2 using a left-shift operation 

> l **Logical Shift (L - left, R - right)** 

**LSL C Operand 0 LSR 0 Operand C X X** (C and X are in Condition Code Register) **Arithmetic Shiftrithmetic ShiftShifthift ASL C Operand 0 ASR Operand C X X** (ASR preserves sign bit) 

l **Arithmetic Shiftrithmetic ShiftShifthift** 

**40 Computer Systems and Professional Practice - Assembler** 

## Examples of Logical Instructions - Rotates 

Note the difference between rotating (RO) and rotating through extend bit (ROX) - what does ROX achieve? 


![](images/assembler/Slide_41_Image_2.png)

> **[Visual Context: Slide_41_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** X1 and X2 are connected to Operand and X3 by blue lines, implying a dependency or flow between these elements.
> **Pedagogical Value:** This image is from a computer systems lecture and does not represent a traditional CSP or constraint graph. It shows assembly language code and labels like 'ROtate through eXtend bit' which relates to computational concepts rather than constraint-based programming.



**----- Start of picture text -----**<br>
l ROtate<br>ROL ROR<br>Operand C<br>C Operand<br>X<br>X<br>l ROtate through eXtend bit<br>ROXR<br>ROXL<br>X Operand Operand X<br>**----- End of picture text -----**<br>


**41** 

**Computer Systems and Professional Practice - Assembler** 

4. Branch Instructions 

Branch instructions cause the processor to branch (jump / GOTO) the labelled address The instruction can test the state of the CCR bits and branch if a certain condition is met CCR flags are set by the previous instruction 

Form: Bcc <label>     (where cc is a condition code) ← If a branch is taken, [PC] label 

**42 Computer Systems and Professional Practice - Assembler** 

## Examples of Branch Instructions 

**15 branch instructions, including:** 

**BRA branch unconditionally BCC branch on carry clear** ( _C_ ) **BCS branch on carry set** ( _C_ ) **BEQ branch on equal** ( _Z_ ) **BGE branch on greater than or equal** ( _N_ . _V_ + _N_ . _V_ ) 

**… BPL branch on plus (ie positive) BVC branch on overflow clear** ( _N_ ) **BVS branch on overflow set** ( _V_ ) ( _V_ ) 

**43 Computer Systems and Professional Practice - Assembler** 

Subroutines and Stacks 


![](images/assembler/Slide_44_Image_1.png)


## Subroutines 

Subroutines are useful for frequently used sections of a program Write (and debug) a subroutine once, and use that program code whenever it is needed 

Reduces program size 

Improves readability 

**JSR <label> Jump to SubRoutine** 

**RTS** 

**Return from SubRoutine** 

**45 Computer Systems and Professional Practice - Assembler** 

## Subroutine Example 

Can you see how subroutines work here - what assumption do you make when you return from a subroutine? 


![](images/assembler/Slide_46_Image_2.png)

> **[Visual Context: Slide_46_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** Interconnected nodes represent constraints between variables and constraints
> **Pedagogical Value:** Visual aids for illustrating constraint-based systems



**----- Start of picture text -----**<br>
JSR FCHAR<br>FCHAR<br>JSR FCHAR<br>FCHAR<br>FCHAR<br>JSR FCHAR<br>FCHAR<br>**----- End of picture text -----**<br>


## **Problem - we need to know where to return** 

**46 Computer Systems and Professional Practice - Assembler** 

## Subroutines and Stacks 

A stack can be used to capture the last in first out (LIFO) aspect of the assumption we were making 

**The stack is a last in** 


![](images/assembler/Slide_47_Image_3.png)


**----- Start of picture text -----**<br>
Then push (add) new value:<br>first out structure. As<br>SP 422<br>before, A7 points to<br>291<br>the Top Of Stack.<br>. [..]<br>992<br>42<br>Say, initially:<br>Stack Pointer  Then pop (remove) value:<br>291<br>(A7)<br>. [..]<br>SP 291<br>992<br>42 . [..]<br>992<br>42<br>**----- End of picture text -----**<br>


**47** 

**Computer Systems and Professional Practice - Assembler** 

Use of Stack for Subroutine Calls 

Subroutine Call (JSR) 

Saves (pushes) the contents of the PC on the stack 

Puts start address of subroutine in PC 

Return from Subroutine (RTS) 

Restores (pops) the return address from the stack and puts it in PC 

So the stack stores where to return from a subroutine 

A subroutine can call another subroutine - we have multiple return addresses on the stack in this case 

**48 Computer Systems and Professional Practice - Assembler** 

Addressing Modes 


![](images/assembler/Slide_49_Image_1.png)


## Addressing Modes 

How we tell the computer where to find data it needs 

Need to organise application data 

Some data never changes, some is variable and some needs to be located within a data structure, e.g., list, table or array 

In 68008 systems data can be located in a data register, within the instruction itself or in external memory 

Addressing modes have expressive power 

Provide data directly 

Specify exactly where data is 

Specify how to go about finding data 

**Computer Systems and Professional Practice - Assembler** 

**50** 

# Human “Addressing Modes” 

“Here’s £100” (literal value) 

“Get the cash from Room 119” (absolute address) 

“Go to Room 26 and they’ll tell you where to get the cash” (indirect address) 

“Go to Room 42 and get the cash from the fifth room to the right” (relative address) 

**51 Computer Systems and Professional Practice - Assembler** 

## 68008 Addressing Modes 

1.  Data or Address Register Direct 

2.  Immediate Addressing 

3.  Absolute Addressing 

4.  Address Register Indirect - five variations 

5.  Relative Addressing 

**52** 

**Computer Systems and Professional Practice - Assembler** 

## 1. Data or Address Register Direct 

Perhaps the simplest addressing mode to comprehend if you understand the 68008 architecture The address of an operand is specified by either a data register or an address register 

**Example 1:** 

**move    D3, D2 D3 D2** 

**Example 2:** 

**move    D3, A2** 


![](images/assembler/Slide_53_Image_6.png)


**----- Start of picture text -----**<br>
D3 A2<br>**----- End of picture text -----**<br>


**53 Computer Systems and Professional Practice - Assembler** 

2. Immediate Addressing 

The operand forms part of the instruction and remains constant throughout the execution of a program 

**move.b    #$42, D5** 

**$42 D5** 

The above puts the hex value 42 into register D5 

Note the # symbol! 

**← [D5] $42** 

**54 Computer Systems and Professional Practice - Assembler** 

3. Absolute Addressing 

# The operand specifies the location in memory explicitly, meaning that no further processing required 

**move.l    D2, $7FFF0** 


![](images/assembler/Slide_55_Image_3.png)


**----- Start of picture text -----**<br>
D2<br>**----- End of picture text -----**<br>


**$7FFF0** 

**← [MS(7FFF0)] [D2]** 

Absolute addressing does not allow position independent code because a program will consistently use the same memory address 

Note there is no # symbol 

**55 Computer Systems and Professional Practice - Assembler** 

## 4. Address Register Indirect 

Address Register Indirect 

**move     (A0), D3** Address Register Indirect with offset 

**move     7F(A1), D3** Post-Incrementing Address Register Indirect 

**move.b  (A0)+, D3** 

**56 Computer Systems and Professional Practice - Assembler** 

4. Address Register Indirect 

Pre-Decrementing Address Register Indirect 

**move.b  -(A0), D3** Indexed Addressing 

**move.l   1F(A0, A1), D3** 

**57** 

**Computer Systems and Professional Practice - Assembler** 

Address Register Indirect 

**move  (A0), D3** 


![](images/assembler/Slide_58_Image_2.png)


**----- Start of picture text -----**<br>
A0 D3<br>**----- End of picture text -----**<br>


Means take the contents of address register A0 and use this number as the address at which the data will be found. Move this data to register D3 

General form: **move (Ai), <ea>** Remember <ea> is an effective address and can be Dj, (Aj), etc... 

**58 Computer Systems and Professional Practice - Assembler** 

## Address Register Indirect with Offset 

**move 7F(A1), D3** 


![](images/assembler/Slide_59_Image_2.png)

> **[Visual Context: Slide_59_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Grid 9x9
> **Logic:** Arrow from A1 to + symbol, arrow from + to D3, grid 9x9, + to D3
> **Pedagogical Value:** High (clear, educational, specific to CSP concept)



**----- Start of picture text -----**<br>
$7F<br>A1 + D3<br>**----- End of picture text -----**<br>


Means take the contents of address register A1, add to this number a (16-bit two's complement) constant and use this result as the address at which the data will be found. Move this data to register D3 

General form: **move d16(Ai), <ea>** 

This is where d16 is a 16-bit two's complement number 

**59 Computer Systems and Professional Practice - Assembler** 

Post-Incrementing Address Register Indirect 

**move.b  (A0)+, D3** 


![](images/assembler/Slide_60_Image_2.png)


**----- Start of picture text -----**<br>
+ A0 D3<br>**----- End of picture text -----**<br>


Means take the contents of address register A0, use this number as the address at which the data will be found. Move this data to register D3 and increment A0 

General form: **move (Ai)+, <ea>** 

Amount by which address register is incremented depends on the type of data being moved, i.e., 1 for bytes, 2 for words, 4 for long words 

**60 Computer Systems and Professional Practice - Assembler** 

## Pre-Decrementing Address Register Indirect 

**move.b  -(A0), D3** 


![](images/assembler/Slide_61_Image_2.png)


**----- Start of picture text -----**<br>
-<br>A0 D3<br>**----- End of picture text -----**<br>


Means decrement the contents of address register A0, and use this number as the address at which the data will be found. Move this data to register D3. 

General form: **move -(Ai), <ea>** 

Amount by which the address register is decremented depends on the type of data being moved 

**61 Computer Systems and Professional Practice - Assembler** 

## Indexed Addressing 

**move.l  $1F(A0, A1), D3** 


![](images/assembler/Slide_62_Image_2.png)

> **[Visual Context: Slide_62_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** Arrows indicate flow between nodes, connecting A0, $1F, and D3.
> **Pedagogical Value:** This image is from a computer systems lecture, illustrating a constraint graph for solving Sudoku using constraint programming.



**----- Start of picture text -----**<br>
A0 $1F<br>A1 + + D3<br>**----- End of picture text -----**<br>


Means add the contents of address register A0 to A1, add to this the (8-bit two's complement) hex constant 1F and use this number as the address at which the data will be found. Move this data to register D3. 

General form: **move d8(Ai, Xj), <ea>** 

Xj can be an address or data register, **d8** is an 8-bit two's complement constant 

**62 Computer Systems and Professional Practice - Assembler** 

## Indexed Addressing Example 

Imagine you’re using a 2D-array to track the number of lectures you have, e.g., the number of lectures on Friday Week 2 is located at DIARY+2*7+5 


![](images/assembler/Slide_63_Image_2.png)

> **[Visual Context: Slide_63_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** D0 points to start of D1, D0 is now a no. of days, D1 is now a no. of lectures
> **Pedagogical Value:** reserve 28 bytes (4 weeks)



**----- Start of picture text -----**<br>
0 (Sun) 1 (Mon) 2 (Tue) 3 (Wed) 4 (Thu) 5 (Fri) 6 (Sat)<br>Week 0 0 6 7 3 5 8 0<br>Week 1 0 4 5 2 6 6 0<br>Week 2 0 (location  6 6 3 5 7 (location  0<br>DIARY+14) DIARY+19)<br>Week 3 0 7 4 1 7 5 0<br>| pre:  week number in D0<br>| post: D1 contains number of lectures on Tuesday in week D0<br>lecsOnTue:  lea  DIARY , A0  | A0 points to start of DIARY<br>mulu  #7, D0  | D0 is now a no. of days<br>move.b  #2(A0,D0),D1  | D1 is now a no. of lectures<br>rts<br>DIARY:  DS.B  28  | reserve 28 bytes (4 weeks)<br>| (data initialised elsewhere)<br>**----- End of picture text -----**<br>


**63 Computer Systems and Professional Practice - Assembler** 

## 5. Relative Addressing 

**move d16(PC), D3** 


![](images/assembler/Slide_64_Image_2.png)

> **[Visual Context: Slide_64_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** Each node connects to multiple others via edges with specific labels.
> **Pedagogical Value:** This image visually represents how constraints (represented by nodes and edges) apply to a Sudoku problem, demonstrating a constraint graph structure.



**----- Start of picture text -----**<br>
d16<br>PC + D3<br>**----- End of picture text -----**<br>


Code like this contains no absolute addresses, i.e., it uses only addresses relative to the current program counter, and therefore can be placed anywhere in memory 

This addressing mode can be used to write “position independent code” 

Be careful - small addressing errors can have big consequences 

**64 Computer Systems and Professional Practice - Assembler** 

## The Accumulator Example 

The example below shows how the use of an alternative addressing mode can reduce the work we have to do in developing elegant assembler programs 

## **Original (pseudo code) Assembly language version** 


![](images/assembler/Slide_65_Image_3.png)

> **[Visual Context: Slide_65_Image_3.png]**
> **Category:** Algorithm/Data Structure Visualization
> **Core Concept:** Grid/Array/Data Structure Analysis
> **Structural Elements:** Grid/Array/Data Structure, Loop/Function/Algorithm
> **Logic:** Sequential flow of data processing
> **Pedagogical Value:** Visual explanation of algorithmic concepts



**----- Start of picture text -----**<br>
int N  move.l  N , D1  | load D1 with number of items<br>int W[100]  movea.l  #W , A2  | load A2 with addr. of 1st item<br>int i, sum  clr.l  D0  | D0 used to accumulate sum<br>loop: add.w  (A2), D0  | add next number from array<br>sum = 0  adda.l #2, A2  | increment A2: point to next word<br>for i = 0 to N-1<br>subq.l #1, D1  | decrement counter<br>sum = sum + W[i]<br>bgt  loop  | if D1 > 0 then branch to loop<br>move.l D0,  sum | store result in sum<br>N:  DS.L  1<br>W:  DS.W  100  | (data initialised elsewhere)<br>sum:  DS.L  1<br>or, the two boxed lines could be the more optimal…<br>loop: add.w  (A2) + , D0  | also increments A2<br>**----- End of picture text -----**<br>


**65 Computer Systems and Professional Practice - Assembler** 

## Fetch-Decode-Execute Revisited 

Having studied assembler and addressing modes, we can consider the fetch-decode -execute cycle in it’s full form Elements of this might not fit together perfectly until we’ve explored memory system and input-output mechanisms We’ll be back!! 


![](images/assembler/Slide_66_Image_2.png)

> **[Visual Context: Slide_66_Image_2.png]**
> **Category:** Constraint Graph
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** Indirect through multiple operations and address calculation
> **Pedagogical Value:** Instrruction complete, fetch next instruction



**----- Start of picture text -----**<br>
Indirection<br>Indirection<br>Instruction Operand Operand<br>fetch fetch store<br>Multiple Multiple<br>operands results<br>Instruction Instruction Operand Operand<br>Data<br>Interrupt<br>address operation address address Interrupt<br>Operation check<br>calculation decoding calculation calculation<br>No<br>Instruction complete, Return for string<br>interrupt<br>fetcth next instruction or vector data<br>**----- End of picture text -----**<br>


Reproduced from: W.Stallings, “Computer Organization and Architecture”, 9th Edition, Pearson, 2013 

**66 Computer Systems and Professional Practice - Assembler** 


![](images/assembler/Slide_67_Image_0.png)

> **[Visual Context: Slide_67_Image_0.png]**
> **Category:** Technical
> **Core Concept:** Sudoku as CSP
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Pedagogical Value:** No specific pedagogical value present.



