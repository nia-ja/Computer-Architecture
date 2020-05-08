"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    # TASK 1: Add the constructor
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    #ram 00-FF (256 bytes of memory)
        self.reg = [0] * 8      #registers
        self.pc = 0             #program counter/current instruction
        self.ir = 0             #instruction register/currently executing instruction
        self.instruction = {   #move to separate file
            0b00000001: 'HLT',
            0b10000010: 'LDI',
            0b01000111: 'PRN'
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            # LDI: load "immediate", store a value in a register, or "set this register to this value"
            0b10000010, # LDI R0,8 (the machine code value of the instruction aka opcode)
            0b00000000,
            0b00001000,
            # PRN: a pseudo-instruction that prints the numeric value stored in a register
            0b01000111, # PRN R0
            0b00000000,
            # HLT: halt the CPU and exit the emulator
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    ## TASK 2: Add method ram_read() and ram_write() that access the RAM inside the CPU object
    ## ram_read() should accept the address to read and return the value stored there
    def ram_read(self, MAR): #memory address register
         return self.ram[MAR] # the Memory Address Register (MAR) - contains the address that is being read or written to.

    ## ram_write() should accept a value to write, and the address to write it to
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR # the Memory Data Register (MDR) - contains the data that was read or the data to write
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    ## TASK 3: Implement the core of CPU's run() method
    def run(self):
        """Run the CPU."""
        halted = False
        while not halted:
            # the Instruction Register (store the result in it)
            IR = self.instruction[self.ram_read(self.pc)]
            # Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them
            op1 = self.ram_read(self.pc + 1) # register location
            op2 = self.ram_read(self.pc + 2) # number to save

            # depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec

            # Add the LDI instruction
            # Sets the value of a register to an integer
            # 3 bytes
            if IR == 'LDI':
                self.reg[op1] = op2 # save op2 to location reg[op1]
                self.pc += 3
            # Add the PRN instruction
            # Print numeric value stored in the given register
            # Print to the console the decimal integer value that is stored in the given register
            # 2 bytes
            elif IR == 'PRN':
                # look at the next line in memory
                # print the number thats in that spot
                print(self.reg[op1])
                self.pc += 2
            # exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded
            # 1 byte
            elif IR == 'HLT':
                halted = True
                self.pc += 1

# test = CPU()
# test.load()
# test.run()