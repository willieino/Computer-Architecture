"""CPU functionality."""

import sys


ram = [0] * 256
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]

registers[7] = 255  #hex(255)
SP = registers[7] # STACK POINTER (SP) R7
IS = registers[6] # INTERRUPT STATUS (IS) R6
IM = registers[5] # INTERRUPT MASK (IM) R5

R0 = registers[0]
R1 = registers[1]
R2 = registers[2]
R3 = registers[3]
R4 = registers[4]
R5 = registers[5]
R6 = registers[6]
R7 = registers[7]

IR = 0 # contains copy of currently executing command
PC = 0
FL = 0
HLT = 1
## ALU ops
 
ADD = 10100000 
SUB = 10100001 
MUL = 10100010 
DIV = 10100011 
MOD = 10100100 

INC = 1100101 
DEC = 1100110 

CMP = 10100111 

AND = 10101000 
NOT = 1101001 
OR  = 10101010 
XOR = 10101011 
SHL = 10101100 
SHR = 10101101  

## Other
NOP = 0
LDI = 10000010
LD = 10000011
ST =  10000100 
PUSH = 1000101
POP = 1000110

PRN = 1000111
PRA = 1001000

## PC mutators

CALL = 1010000
RET = 10001

INT = 1010010
IRET = 10011

JMP = 1010100 
JEQ = 1010101 
JNE = 1010110 
JGT = 1010111 
JLT = 1011000 
JLE = 1011001
JGE = 1011010  

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
        self.PC = 0
        self.FL = 0
        
    def ram_read(self, mar):
        mdr = ram[mar]
        return mdr
      
    def ram_write(self, mar, mdr): 
        ram[mar] = mdr

    # RETURNS A 8BIT BINARY
    def p8(self, v):
        return "{:08b}".format(v)

    def load_memory(self, ram, filename):
        address = 0
        try:
            with open(filename) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_number = comment_split[0]
                    if possible_number == '' or possible_number == '\n':
                        continue
                    instruction = int(possible_number)
                    ram[address] = instruction 
                    address += 1
            return ram
        except IOError:  #FileNotFoundError
            print('I cannot find that file, check the name')
            sys.exit(2)

    def print_registers(self):
        print("registers[0]: ", self.registers[0])
        print("registers[1]: ", self.registers[1])
        print("registers[2]: ", self.registers[2])
        print("registers[3]: ", self.registers[3])
        print("registers[4]: ", self.registers[4])
        print("registers[5]: ", self.registers[5])
        print("registers[6]: ", self.registers[6])
        print("registers[7]: ", self.registers[7])


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.FL,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
            ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print() 

    def run(self, ram):
        """Run the CPU."""
        running = True
        IR = 0
        self.PC = 0
        
        self.ram_read(self.PC)
        
        while running:
            #self.trace()
            command = ram[self.PC]
            
            if command == HLT:
                running = False
            
            elif command == LDI:
                op = ram[self.PC]
                register = ram[self.PC + 1]
                value = ram[self.PC + 2]
                self.registers[register] = value
                self.PC += 3
               
            elif command == PRN:
                # read the register number
                register = int(str(ram[self.PC + 1]), 2)
                # get the value that is at this register
                value = self.registers[register]
                # print the value
                print(int(str(value), 2))
                self.PC += 2

            elif command == ADD:
                # get the address for both of the values 
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                # using the address retrieve the integer values then add them 
                sum = int(str(self.registers[first_register]), 2) + int(str(self.registers[second_register]), 2)
                sum = (bin(sum))[2:]
                # save the sum to the first register
                self.registers[first_register] = sum
                self.PC += 3

            elif command == SUB:
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                diff = self.registers[first_register] - self.registers[second_register]
                self.registers[first_register] = diff
                self.PC += 3

            elif command == MUL:
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                # Multiply the first register by the second register
                prod = self.registers[first_register] * self.registers[second_register]
                # save the product to the first register
                self.registers[first_register] = prod
                self.PC += 3

            elif command == DIV:
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                # make sure we arent trying to divide by zero
                if value_b > 0:
                    value = value_a // value_b
                    self.registers[first_register] = value
                    # advance the program counter
                    self.PC += 3
                else:
                    print("Unable to divide by zero")
                    running = False

            elif command == PUSH:
                self.registers[7] = ( self.registers[7] - 1 ) % 255
                SP = self.registers[7]
                register_address = ram[self.PC + 1]
                value = self.registers[register_address]
                ram[SP] = value              
                self.PC += 2

            elif command == POP:
                SP = self.registers[7]
                value = ram[SP]
                register_address = int(str(ram[self.PC + 1]), 2)
                self.registers[register_address] = value
                self.registers[7] = ( SP + 1 ) % 255
                self.PC += 2

            elif command == MOD:
                pass
                # code here
                #             
            elif command == INC:
                register = ram[self.PC + 1]
                value = self.registers[register]
                value = hex(value)
                self.registers[register] = value
                self.PC += 2

            elif command == JMP:
                pass # not finished with this
                register = ram[self.PC + 1]
                value = self.registers[register]
                self.PC = value
                #value += 2 

            elif command == CALL:
                # push address of instruction after CALL to stack
                # get the register address from ram
                register_address = ram[self.PC + 1]
                # check contents for the address we are going to jump to
                address_to_jump_to = int(str(self.registers[register_address]), 2)
                # save the next instruction address for the RETurn
                next_instruction_address = bin(self.PC + 2)
                next_instruction_address = int(next_instruction_address[2:])
                #
                self.registers[7] = (self.registers[7] - 1) % 255
                # update the stack pointer
                SP = self.registers[7]
                # write the next instruction address to the stack in ram
                ram[SP] = next_instruction_address
                # move program counter to new location
                self.PC = address_to_jump_to
  
            elif command == RET:
                # get the location of our return_to_address
                SP = self.registers[7]
                # save the address from the stack
                address_to_return_to = ram[SP]
                # update thestack pointer
                self.registers[7] = ( SP + 1 ) % 255
                # set the program counter to its new location address
                self.PC = int(address_to_return_to)
                self.PC = int(str(self.PC), 2)
            else:
                running = False    

