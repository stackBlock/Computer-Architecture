# """CPU functionality."""

import sys

LDI = 0b10000010 # load immediate
PRN = 0b01000111 # print value of integer saved to register address
HLT = 0b00000001 # halt program
MUL = 0b10100010 # multiplication
PUSH = 0b01000101 # 69
POP = 0b01000110 # 70
CALL = 0b01010000 # 80
RET = 0b00010001 # 17 - return
ADD = 0b10100000 # 160


# # Day 1: Get print8.ls8 running
# #  Inventory what is here
# #  Implement the CPU constructor
# #  Add RAM functions ram_read() and ram_write()
# #  Implement the core of run()
# #  Implement the HLT instruction handler
# #  Add the LDI instruction
# #  Add the PRN instruction

# class CPU:
#     """Main CPU class."""

#     def __init__(self):
#         """Construct a new CPU."""
#         self.pc = 0                                 # CPU Constructor 
#         self.reg = [0] * 8 
#         self.ram = [0] * 256 


#     def ram_read(self, mar):                        # ram_read() function
#         return self.ram[mar]

    
#     def ram_write(self,mar,mdr):                    # ram_write() function
#         self.ram[mar] = mdr

    
#     def load(self):
#         """Load a program into memory."""

#         address = 0

#         # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000,
#             0b00001000,
#             0b01000111, # PRN R0
#             0b00000000,
#             0b00000001, # HLT
#         ]

#         # program = [
#         #     # From print8.ls8
#         #     ob10000010 # LDI R0,8
#         #     0b00000000
#         #     0b00001000
#         #     0b10000010 # LDI R1,9
#         #     0b00000001
#         #     0b00001001
#         #     0b10100010 # MUL R0,R1
#         #     0b00000000
#         #     0b00000001
#         #     0b01000111 # PRN R0
#         #     0b00000000
#         #     0b00000001 # HLT
#         # ]        

#         for instruction in program:
#             self.ram[address] = instruction
#             address += 1


#     def alu(self, op, reg_a, reg_b):
#         """ALU operations."""

#         if op == "ADD":
#             self.reg[reg_a] += self.reg[reg_b]
#         #elif op == "SUB": etc
#         else:
#             raise Exception("Unsupported ALU operation")

#     def trace(self):
#         """
#         Handy function to print out the CPU state. You might want to call this
#         from run() if you need help debugging.
#         """

#         print(f"TRACE: %02X | %02X %02X %02X |" % (
#             self.pc,
#             #self.fl,
#             #self.ie,
#             self.ram_read(self.pc),
#             self.ram_read(self.pc + 1),
#             self.ram_read(self.pc + 2)
#         ), end='')

#         for i in range(8):
#             print(" %02X" % self.reg[i], end='')

#         print()

#     def run(self):
#         """Run the CPU."""
#         HLT = 0b00000001                            # run() function
#         LDI = 0b10000010
#         PRN = 0b01000111

#         running = True

#         while running:
#             instruction = self.ram_read(self.pc)
#             opr_a = self.ram_read(self.pc + 1)
#             opr_b = self.ram_read(self.pc + 2)

#             if instruction == HLT:                  # HLT instruction handler
#                 running = False
#                 self.pc +=1
                

#             elif instruction == LDI:                # LDI instruction handler
#                 self.reg[opr_a] = opr_b
#                 self.pc += 3 
            
#             elif instruction == PRN:                # PRN instruction handler
#                 print(self.reg[opr_a])
#                 self.pc += 2
            
#             else:
#                 print(f"bad command: {bin(instruction)}")
#                 running = False

# print(sys.argv)





class CPU:
    """Main CPU class."""

    def __init__(self):
        self.memory = [0]*256
        self.register = [0]*8
        self.pc = 0 # program counter
        self.register[7] = 0b11110100 # 244
        self.run_logic = True

    def load(self):
        if len(sys.argv) != 2:                                  # Load into memory
            print("to use: python ls8.py examples/mult.ls8")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split('#')             # extract number from file
                    num = comment_split[0].strip()

                    if num != "":                               # print out asm instruction
                        print(f'{num}')
                        value = int(num, 2)                     # save number to memory if exists
                        self.memory_write(value, address)
                        address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, register_a, register_b):
        """
        ALU operations. (arithmetic/logic unit)
        """

        if op == "ADD":
            self.register[register_a] += self.register[register_b]
        elif op == "MUL":
            self.register[register_a] *= self.register[register_b]
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
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

    def memory_read(self, MAR):
        return self.memory[MAR]

    def memory_write(self, MDR, MAR):
        self.memory[MAR] = MDR
        return

    def instruction_switch_run(self, IR, operand_a, operand_b):
        if IR == LDI:
            self.register[operand_a] = operand_b
            self.pc += 3                                       
        elif IR == PRN:
            print(self.register[operand_a])
            self.pc += 2
        elif IR == MUL:                                         
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3
        elif IR == HLT:
            self.run_logic = False
        elif IR == PUSH:
            value = self.register[operand_a]
            self.register[7] -= 1
            self.memory_write(value, self.register[7])
            self.pc += 2
        elif IR == POP:
            self.register[operand_a] = self.memory_read(self.register[7])
            value = self.register[operand_a]
            self.register[7] += 1
            self.pc += 2
        elif IR == CALL:
            call_address = self.pc + 2
            self.register[7] -= 1
            self.memory_write(call_address, self.register[7])
            self.pc = self.register[operand_a]
        elif IR == RET:
            ret_address = self.register[7]
            self.pc = self.memory_read(ret_address)
            self.register[7] += 1
        elif IR == ADD:                                       
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3
        else:
            print(f"{IR} - command is not available")
            sys.exit()

    def run(self):
        while self.run_logic:                                           # instructions
            IR = self.memory_read(self.pc)
            operand_a = self.memory_read(self.pc + 1)                   # read in integer
            operand_b = self.memory_read(self.pc + 2)                   # receive instruction and perform task
            self.instruction_switch_run(IR, operand_a, operand_b)



# # python ls8.py examples/mult.ls8