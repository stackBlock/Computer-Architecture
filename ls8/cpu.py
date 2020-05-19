"""CPU functionality."""

import sys


# Day 1: Get print8.ls8 running
#  Inventory what is here
#  Implement the CPU constructor
#  Add RAM functions ram_read() and ram_write()
#  Implement the core of run()
#  Implement the HLT instruction handler
#  Add the LDI instruction
#  Add the PRN instruction

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0                                 # CPU Constructor 
        self.reg = [0] * 8 
        self.ram = [0] * 256 


    def ram_read(self, mar):                        # ram_read() function
        return self.ram[mar]

    
    def ram_write(self,mar,mdr):                    # ram_write() function
        self.ram[mar] = mdr

    
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # program = [
        #     # From print8.ls8
        #     ob10000010 # LDI R0,8
        #     0b00000000
        #     0b00001000
        #     0b10000010 # LDI R1,9
        #     0b00000001
        #     0b00001001
        #     0b10100010 # MUL R0,R1
        #     0b00000000
        #     0b00000001
        #     0b01000111 # PRN R0
        #     0b00000000
        #     0b00000001 # HLT
        # ]        

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001                            # run() function
        LDI = 0b10000010
        PRN = 0b01000111

        running = True

        while running:
            instruction = self.ram_read(self.pc)
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)

            if instruction == HLT:                  # HLT instruction handler
                running = False
                self.pc +=1
                

            elif instruction == LDI:                # LDI instruction handler
                self.reg[opr_a] = opr_b
                self.pc += 3 
            
            elif instruction == PRN:                # PRN instruction handler
                print(self.reg[opr_a])
                self.pc += 2
            
            else:
                print(f"bad command: {bin(instruction)}")
                running = False

print(sys.argv)