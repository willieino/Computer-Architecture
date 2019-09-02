"""CPU functionality."""

import sys

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
        self.ram = [0] * 256
        self.IR = 0
        self.PC = 0
        self.FL = 0
        self.OP = 0
        self.SP = 0xF3
        self.ins_set = 0
        self.op_size = 0
        self.stop = False
        self.SP = self.registers[7] # STACK POINTER (SP) R7
        self.IS = self.registers[6] # INTERRUPT STATUS (IS) R6
        self.IM = self.registers[5] # INTERRUPT MASK (IM) R5
        
        self.ops = {
            LDI: self.op_ldi,
            ADD: self.op_add,
            AND: self.op_and,
            CALL: self.op_call,
            CMP: self.op_cmp,
            DEC: self.op_dec,
            DIV: self.op_div,
            HLT: self.op_hlt,
            INC: self.op_inc,
            JEQ: self.op_jeq,
            JMP: self.op_jmp,
            JNE: self.op_jne,
            LD: self.op_ld,
            LDI: self.op_ldi,
            MOD: self.op_mod,
            MUL: self.op_mul,
            NOT: self.op_not,
            OR: self.op_or,
            POP: self.op_pop,
            PRA: self.op_pra,
            PRN: self.op_prn,
            PUSH: self.op_push,
            RET: self.op_ret,
            SHL: self.op_shl,
            SHR: self.op_shr,
            ST: self.op_st,
            SUB: self.op_sub,
            XOR: self.op_xor
        }

    def op_hlt(self, op_a, op_b):
        print("STOP NOW!")
        self.stop = True

    def op_ldi(self, op_a, op_b):
        print("LDI:PC:", self.PC)
        self.registers[op_a] = op_b

    def op_prn(self, op_a, op_b):
        print("PRN:PC:", self.PC)
        print(self.registers[op_a])
    
    def op_mul(self, op_a, op_b):
        print("MUL:PC:", self.PC)
        self.registers[op_a] = (op_a * op_b)
        
    def op_cmp(self, op_a, op_b):
        print("CMP:PC:", self.PC)
        pass
        # get the two register values
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
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
        # advance the progself.ram counter
        self.PC += 3             

    def op_push(self, op_a, op_b):
        print("PUSH:PC:", self.PC)
        pass
        self.registers[7] = ( self.registers[7] - 1 ) % 255
        self.SP = self.registers[7]
        register_address = self.ram[self.PC + 1]
        value = self.registers[register_address]
        self.ram[self.SP] = value              
        self.PC += 2

    def op_pop(self, op_a, op_b):
        print("POP:PC:", self.PC)
        pass
        self.SP = self.registers[7]
        value = self.ram[self.SP]
        register_address = int(str(self.ram[self.PC + 1]), 2)
        self.registers[register_address] = value
        self.registers[7] = ( self.SP + 1 ) % 255
        self.PC += 2

    def op_call(self, op_a, op_b):
        print("CALL:PC:", self.PC)
        pass
        # push address of instruction after CALL to stack
        # get the register address from ram
        register_address = self.ram[self.PC + 1]
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
        self.ram[self.SP] = next_instruction_address
        # move program counter to new location
        self.PC = int(str(address_to_jump_to), 2)

    def op_ret(self, op_a, op_b):
        print("RET:PC:", self.PC)
        pass
        # get the location of our return_to_address
        self.SP = self.registers[7]
        # save the address from the stack
        address_to_return_to = self.ram[self.SP]
        # update thestack pointer
        self.registers[7] = ( self.SP + 1 ) % 255
        # set the program counter to its new location address
        self.PC = int(address_to_return_to)
        self.PC = int(str(self.PC), 2)

    def op_jmp(self, op_a, op_b):
        print("JMP:PC:", self.PC)
        pass
        #pass # not finished with this
        register_address = self.ram[self.PC + 1]
        register_address = int(str(register_address), 2)
        address_to_jump_to = self.registers[register_address]
        address_to_jump_to = int(str(address_to_jump_to), 2)
        self.PC = address_to_jump_to              

    def op_jne(self, op_a, op_b):
        print("JNE:PC:", self.PC)
        pass
        # If `E` flag is clear (false, 0), jump to the address stored in the given register.   
        if self.FL == 0:
            register = self.ram[self.PC + 1]
            value = self.registers[register]
            self.PC = int(str(value), 2) 
        # if the values are not equal advance the program counter
        else:
            self.PC += 2   

    def op_jeq(self, op_a, op_b):
        print("JEQ:PC:", self.PC)
        pass
        # If `equal` flag is set (true), jump to the address stored in the given register.  
        if self.FL == 1:
            register = self.ram[self.PC + 1]
            register = int(str(register), 2)
            value = self.registers[register]
            self.PC = int(str(value), 2) 
        # if the values are not equal advance the program counter
        else:
            self.PC += 2     
        
    def op_ld(self, op_a, op_b):
        print("LD:PC:", self.PC)
        pass
        register_address_a = self.ram[self.PC + 1]
        register_address_b = self.ram[self.PC + 2]
        self.registers[register_address_a] = self.registers[register_address_b]

    def op_pra(self, op_a, op_b):
        print("PRA:PC:", self.PC)
        pass
        # read the register number
        register = int(str(self.ram[self.PC + 1]), 2)
        # get the value that is at this register
        value = self.registers[register]
        # print the value
        letter = self.get_ascii(value)
        print(letter)
        self.PC += 2

    def op_and(self, op_a, op_b):
        print("AND:PC:", self.PC)
        pass
        print("AND:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        temp = int(bin(value_a), 2) & int(bin(value_b), 2)
        print("temp: ", temp)
        self.PC += 3
        
    def op_or(self, op_a, op_b):
        print("OR:PC:", self.PC)
        pass
        print("OR:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        print(bin(value_a))
        print(bin(value_b))
        self.PC += 3

    def op_xor(self, op_a, op_b):
        print("XOR:PC:", self.PC)
        pass
        print("XOR:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        print(bin(value_a))
        print(bin(value_b))
        self.PC += 3

    def op_not(self, op_a, op_b):
        print("NOT:PC:", self.PC)
        pass
        print("NOT:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        print(bin(value_a))
        print(bin(value_b))
        self.PC += 3
    
    def op_shl(self, op_a, op_b):
        print("SHL:PC:", self.PC)
        pass
        print("SHL:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        print(bin(value_a))
        print(bin(value_b))
        self.PC += 3
       

    def op_shr(self, op_a, op_b):
        print("SHR:PC:", self.PC)
        pass
        print("SHR:")
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        print(bin(value_a))
        print(bin(value_b))
        self.PC += 3                    

    def op_add(self, op_a, op_b):
        print("ADD:PC:", self.PC)
        pass
        # get the address for both of the values 
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        # using the address retrieve the integer values then add them 
        sum = int(str(self.registers[first_register]), 2) + int(str(self.registers[second_register]), 2)
        sum = (bin(sum))[2:]
        # save the sum to the first register
        self.registers[first_register] = sum
        self.PC += 3

    def op_st(self, op_a, op_b):
        print("ST:PC:", self.PC)
        pass
        # store the value in register b in the address stored in register a
        # get the two register addresses from the PC
        register_address_a = self.ram[self.PC + 1]
        register_address_b = self.ram[self.PC + 2]
        self.registers[register_address_a] = self.registers[register_address_b]
        self.PC += 3

    def op_sub(self, op_a, op_b):
        print("SUB:PC:", self.PC)
        pass
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        diff = self.registers[first_register] - self.registers[second_register]
        self.registers[first_register] = diff
        self.PC += 3

    def op_mod(self, op_a, op_b):
        print("MOD:PC:", self.PC)
        pass
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        # make sure we arent trying to divide by zero
        if value_b > 0:
            value = value_a // value_b
            self.registers[first_register] = value
            # advance the progself.ram counter
            self.PC += 3
        else:
            print("Unable to divide by zero")
            running = False    

    def op_inc(self, op_a, op_b):
        print("INC:PC:", self.PC)
        pass
        register = self.ram[self.PC + 1]
        value = self.registers[register]
        value = hex(value)
        self.registers[register] = value
        self.PC += 2

    def op_dec(self, op_a, op_b):
        print("DEC:PC:", self.PC)
        pass

    def op_div(self, op_a, op_b):
        print("DIV:PC:", self.PC)
        pass
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        value_a = self.registers[first_register]
        value_b = self.registers[second_register]
        # make sure we arent trying to divide by zero
        if value_b > 0:
            value = value_a // value_b
            self.registers[first_register] = value
            # advance the progself.ram counter
            self.PC += 3
        else:
            print("Unable to divide by zero")
            running = False
            
    def ram_read(self, mar):
        return self.ram[mar]
      
    def ram_write(self, mar, mdr): 
        self.ram[mar] = mdr

    # RETURNS A 8BIT BINARY
    def p8(self, v):
        return "{:08b}".format(v)

    # use this to print letters
    def get_ascii(self, binary_in):
 
        print("binary_in: ", binary_in)
        n = int(str(binary_in), 2)
        n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return n

    def load_memory(self, filename):
        address = 0
        try:
            with open(filename) as file:
                for line in file:
                    comment_split = line.split('#')
                    instruction = comment_split[0]
                    if instruction == '' or instruction == '\n':
                    #if instruction == '':
                        continue
                    first_bit = instruction[0]
                    if first_bit == '0' or first_bit == '1':
                        self.ram[address] = int(instruction[:8], 2)
                        address += 1
                    
                    #instruction = str(possible_number)
                    #instruction = hex(possible_number)
                    #instruction = bin(instruction)
                    #ram[address] = instruction 
                    #address += 1
            return self.ram
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

    def run(self):
        """Run the CPU."""
        running = True
        LDI = 0b10000010
        PRN = 0b01000111        
        HLT = 0b00000001
        self.registers[7] = 255
        #IR = #self.ram_read(self.PC)

        #= 10
        #x = 0
        #while running:
        while not self.stop:
            #x += 1
            self.IR = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)
            
            self.print_registers()
            self.trace()
            print("self.ram: ", self.ram)
            
            self.op_size = self.IR >> 6
            self.ins_set = ((self.IR >> 4) & 0b1) == 1
            print("self.ins_set:", self.ins_set)
            

            print("self.IR:", self.IR)
            if self.IR in self.ops:
                self.ops[self.IR](op_a, op_b)
            
            if not self.ins_set:
                self.PC += self.op_size + 1
            #command = bin(int(ram[self.PC], 2))
            #print("command:", command)
        
            #if command == HLT:
                #running = False 
            

        sys.exit 

