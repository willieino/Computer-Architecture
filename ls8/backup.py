"""CPU functionality."""

import sys


ram = [0] * 256
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]

registers[7] = 255  #hex(255)

IR = 0 # contains copy of currently executing command
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
        self.SP = 0xF3
        self.SP = self.registers[7] # STACK POINTER (SP) R7
        self.IS = self.registers[6] # INTERRUPT STATUS (IS) R6
        self.IM = self.registers[5] # INTERRUPT MASK (IM) R5
        
    def ram_read(self, mar):
        mdr = ram[mar]
        return mdr
      
    def ram_write(self, mar, mdr): 
        ram[mar] = mdr

    # RETURNS A 8BIT BINARY
    def p8(self, v):
        return "{:08b}".format(v)

    # use this to print letters
    def get_ascii(self, binary_in):
 
        print("binary_in: ", binary_in)
        n = int(str(binary_in), 2)
        n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return n

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

    # print the register values, only for debugging
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
            #self.SP,
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
        self.registers[7] = 0xF3
        self.SP = self.registers[7]
        self.ram_read(self.PC)
        
        while running:
            
            self.print_registers()
            self.trace()
            print("ram: ", ram)
            command = ram[self.PC]
        
            if command == HLT:
                running = False
            
            elif command == LD:
                # Loads registerA with the value at the memory address stored in registerB
                # get the two register addresses a and b 

                # take the value of register b and store it in register a 
                register_address_a = ram[self.PC + 1]
                register_address_b = ram[self.PC + 2]
 
                self.registers[register_address_a] = self.registers[register_address_b]

                self.PC += 3

            elif command == LDI:
                op = ram[self.PC]
                register = int(str(ram[self.PC + 1]), 2)
                value = ram[self.PC + 2] 
                self.registers[register] = int(value)
                self.PC += 3         
                
            elif command == PRA:
                # read the register number
                register = int(str(ram[self.PC + 1]), 2)
                # get the value that is at this register
                value = self.registers[register]
                # print the value
                letter = self.get_ascii(value)
                print(letter)
                self.PC += 2

            elif command == PRN:
                # read the register number
                register = int(str(ram[self.PC + 1]), 2)
                # get the value that is at this register
                value = self.registers[register]
                # print the value
                print(int(str(value), 2))
                self.PC += 2

            elif command == AND: 
                print("AND:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                temp = int(bin(value_a), 2) & int(bin(value_b), 2)
                print("temp: ", temp)

                self.PC += 3

            elif command == OR: 
                print("OR:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                print(bin(value_a))
                print(bin(value_b))
                self.PC += 3

            elif command == XOR: 
                print("XOR:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                print(bin(value_a))
                print(bin(value_b))
                self.PC += 3

            elif command == NOT: 
                print("NOT:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                print(bin(value_a))
                print(bin(value_b))
                self.PC += 3

            elif command == SHL: 
                print("SHL:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                print(bin(value_a))
                print(bin(value_b))
                self.PC += 3

            elif command == SHR: 
                print("SHR:")
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                print(bin(value_a))
                print(bin(value_b))
                self.PC += 3                    
            
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
 
            elif command == ST:
                # store the value in register b in the address stored in register a
                # get the two register addresses from the PC
                register_address_a = ram[self.PC + 1]
                register_address_b = ram[self.PC + 2]
                self.registers[register_address_a] = self.registers[register_address_b]
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

            elif command == CMP:
                # get the two register values
                first_register = ram[self.PC + 1]
                second_register = ram[self.PC + 2]
                value_a = self.registers[first_register]
                value_b = self.registers[second_register]
                # compare the values if reg_a is less than reg_b set FL to 00000100
                if value_a < value_b:
                    self.FL = 100
                # compare the values if reg_a is greater than reg_b set FL to 00000010
                elif value_a > value_b:
                    self.FL = 10
                # compare the values if reg_a is equal to reg_b set FL to 00000001
                else:
                    self.FL = 1
                # advance the program counter
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
                self.SP = self.registers[7]
                register_address = ram[self.PC + 1]
                value = self.registers[register_address]
                ram[self.SP] = value              
                self.PC += 2

            elif command == POP:
                self.SP = self.registers[7]
                value = ram[self.SP]
                register_address = int(str(ram[self.PC + 1]), 2)
                self.registers[register_address] = value
                self.registers[7] = ( self.SP + 1 ) % 255
                self.PC += 2

            elif command == MOD:
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
                            
            elif command == INC:
                register = ram[self.PC + 1]
                value = self.registers[register]
                value = hex(value)
                self.registers[register] = value
                self.PC += 2

            elif command == JEQ: 
                # If `equal` flag is set (true), jump to the address stored in the given register.  
                if self.FL == 1:
                    register = ram[self.PC + 1]
                    register = int(str(register), 2)
                    value = self.registers[register]
                    self.PC = int(str(value), 2) 
                # if the values are not equal advance the program counter
                else:
                    self.PC += 2     
            
            elif command == JNE: 
                # If `E` flag is clear (false, 0), jump to the address stored in the given register.   
                if self.FL == 0:
                    register = ram[self.PC + 1]
                    value = self.registers[register]
                    self.PC = int(str(value), 2) 
                # if the values are not equal advance the program counter
                else:
                    self.PC += 2   
            
            elif command == JMP:
                #pass # not finished with this
                register_address = ram[self.PC + 1]
                register_address = int(str(register_address), 2)
                address_to_jump_to = self.registers[register_address]
                address_to_jump_to = int(str(address_to_jump_to), 2)
                self.PC = address_to_jump_to              
                
            elif command == CALL:
                # push address of instruction after CALL to stack
                # get the register address from ram
                register_address = ram[self.PC + 1]
                # check contents for the address we are going to jump to
                register_address = int(str(register_address), 2)
                #print("register_address:", register_address)
                address_to_jump_to = self.registers[register_address]              
                # save the next instruction address for the RETurn
                next_instruction_address = bin(self.PC + 2)
                next_instruction_address = int(next_instruction_address[2:])        
                self.registers[7] = (self.registers[7] - 1) % 255
                # update the stack pointer
                self.SP = self.registers[7]
                # write the next instruction address to the stack in ram
                ram[self.SP] = next_instruction_address
                # move program counter to new location
                self.PC = int(str(address_to_jump_to), 2)
 
            elif command == RET:
                # get the location of our return_to_address
                self.SP = self.registers[7]
                # save the address from the stack
                address_to_return_to = ram[self.SP]
                # update thestack pointer
                self.registers[7] = ( self.SP + 1 ) % 255
                # set the program counter to its new location address
                self.PC = int(address_to_return_to)
                self.PC = int(str(self.PC), 2)
            else:
                running = False    

