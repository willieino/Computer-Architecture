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
HLT = bin( 0b00000001 )
## ALU ops
 
ADD = 10100000 
SUB = 10100001 
MUL = 10100010 
DIV = 10100011 
MOD = 10100100 

INC = bin( 0b01100101 ) 
DEC = bin( 0b01100110) 

CMP = bin( 0b10100111) 

AND = 10101000 
NOT = bin( 0b01101001 ) 
OR  = 10101010 
XOR = 10101011 
SHL = 10101100 
SHR = 10101101  

## Other

NOP = bin( 0b00000000)
HLT = bin( 0b00000001 ) 
LDI = 10000010
LD = 10000011
ST =  10000100 
PUSH = bin( 0b01000101 )
POP = bin( 0b01000110 )
PRN = bin( 0b01000111 )
PRA = bin( 0b01001000 )
LDI = 10000010

## PC mutators

CALL = bin( 0b01010000 )
RET = bin( 0b00010001 )

INT = bin( 0b01010010 )
IRET = bin( 0b00010011)

''' JMP = 01010100 
JEQ = 01010101 
JNE = 01010110 
JGT = 01010111 
JLT = 01011000 
JLE = 01011001
JGE = 01011010  '''

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
        
    def ram_read(self, addr):
        #addr = self.addr
        value = bin( ram[addr] )

        return value
        # code here


    def ram_write(self, addr, value):
        #addr = self.addr
        #value = self.value
        return
        # code here

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

    def alu(self, op, reg_a, reg_b):
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
            raise Exception("Unsupported ALU operation")
 
    ''' def trace(self):
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
            #), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print() '''

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
                print("LDI", op)
                registers[ram[pc + 1]] = ram[pc + 2]
                R0 = int(ram[pc + 2])
                print("R0:", R0)
                pc += 3
            elif command == PRN:
                num = int(R0)
                #num = ram[pc + 1]
                print("num:", num)
                pc += 2
            elif command == ADD:
                # send it to the ALU
                op = ram[pc]
                R0 = ram[pc + 1]
                R1 = ram[pc + 2] 
                alu(op, R0, R1) 
                pc += 3          
            elif command == SUB:
                pass
                # code here            
            elif command == MUL:
                print("mul:")
                # code here            
            elif command == DIV:
                pass
                # code here            
            elif command == MOD:
                pass
                # code here            
            elif command == INC:
                pass
                # code here  
                # 
            else:
                running = False          
