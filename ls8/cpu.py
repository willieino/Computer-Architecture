"""CPU functionality."""

import sys


ram = [0] * 256
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
registers[7] = 0xF4
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

pc = 0
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

CALL = 101000
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
        """Construct a new CPU."""
        ram = [0] * 256
        registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
        registers[7] = 0xF4
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

        pc = 0
        FL = 0
        
    def ram_read(self, mar):
        mdr = ram[mar]
        #value = ram[addr]
        print("ram_read: ", mdr)
        return mdr
      
    def ram_write(self, mar, mdr): 
        ram[mar] = mdr

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

    ''' def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        #pass
        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]     
        elif op == MUL:
            self.reg[reg_a] * self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] // self.reg[reg_b]
        elif op == MOD:
            pass
            # sub code here
        elif op == INC:
            pass
            # sub code here
        elif op == DEC:
            pass
            # sub code here
        elif op == CMP:
            pass
            # sub code here
        elif op == AND:
            pass
                # sub code here
        elif op == NOT:
            pass
            # sub code here
        elif op == OR:
            pass
                # sub code here
        elif op == XOR:
            pass
            # sub code here
        elif op == SHL:
            pass
                # sub code here
        elif op == SHR:
            pass
            # sub code here      
        else:
            raise Exception("Unsupported ALU operation") '''
 
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

    def run(self, ram):
        """Run the CPU."""
        running = True
        IR = 0
        pc = 0
        self.ram_read(pc)
    
        while running:
            command = ram[pc]
            print("command: ", command)
            print("this is ram:", ram)
            if command == HLT:
                running = False
            
            elif command == LDI:
                op = ram[pc]
                register = ram[pc + 1]
                value = ram[pc + 2]
                registers[register] = value
                pc += 3
                print("LDI", op)
               
            elif command == ADD:
                first_register = ram[PC + 1]
                second_register = ram[PC + 2]
                sum = registers[first_register] + registers[second_register]
                registers[first_register] = sum
                PC += 3
            elif command == PRN:
                print("PRN: ", command)
                # read the register number
                register = ram[pc + 1]
                # get the value that is at this register
                value = registers[register]
                # print the value
                print(value)
                pc += 2
            elif command == ADD:
                op = ram[pc]
                R0 = ram[pc + 1]
                R1 = ram[pc + 2] 
                sum = R0 + R1
                registers[0] = sum
                pc += 3          
            elif command == SUB:
                op = ram[pc]
                R0 = ram[pc + 1]
                R1 = ram[pc + 2] 
                diff = R0 - R1
                registers[0] = diff
                pc += 3                 
            elif command == MUL:
                print("mul:")
                first_register = ram[pc + 1]
                second_register = ram[pc + 2]
                prod = first_register * second_register
                registers[0] = prod
                print("prod:", prod)
                pc += 3           
            elif command == DIV:
                first_register = ram[pc + 1]
                second_register = ram[pc + 2]
                value_a = registers[first_register]
                value_b = registers[second_register]
                if value_b > 0:
                    value = value_a // value_b
                    registers[first_register] = value
                    pc += 3
                else:
                    print("Unable to divide by zero")
                    running = False
                      
            elif command == MOD:
                pass
                # code here            
            elif command == INC:
                register = ram[pc + 1]
                value = registers[register]
                value += 1 
                registers[register] = value
                pc += 2
            else:
                running = False    

#s = bin(n) 
      
    # removing "0b" prefix 
   # s1 = s[2:]       
