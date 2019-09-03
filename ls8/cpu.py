"""CPU functionality."""

import sys
import binascii

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
POP = 0b010001
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001        
POP = 0b01000110
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

    def op_add(self, op_a, op_b):
        # get the address for both of the values 
        # using the address retrieve the integer values then add them 
        sum = self.registers[op_a] + self.registers[op_b]
        # save the sum to the first register
        self.registers[op_a] = sum

    def op_and(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        temp = int(bin(value_a), 2) & int(bin(value_b), 2)
        self.registers[op_a] = temp

    def op_cmp(self, op_a, op_b):
        # get the two register values
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        # compare the values if reg_a is less than reg_b set FL to 00000100
        if value_a < value_b:
            self.FL = 100
        # compare the values if reg_a is greater than reg_b set FL to 00000010
        elif value_a > value_b:
            self.FL = 10
        # compare the values if reg_a is equal to reg_b set FL to 00000001
        else:
            self.FL = 1

    def op_call(self, op_a, op_b):
        # push address of instruction after CALL to stack
        # get the register address from ram
        register_address = self.ram[self.PC + 1]
        # check contents for the address we are going to jump to
        address_to_jump_to = self.registers[register_address]              
        # save the next instruction address for the RETurn
        next_instruction_address = self.PC + 2   
        self.registers[7] = (self.registers[7] - 1) % 255
        # update the stack pointer
        self.SP = self.registers[7]
        # write the next instruction address to the stack in ram
        self.ram[self.SP] = next_instruction_address
        # move program counter to new location
        self.PC = address_to_jump_to

    def op_dec(self, op_a, op_b):
        dec = self.registers[op_a] - 1
        self.registers[op_a] = dec

    def op_div(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        # make sure we arent trying to divide by zero
        if value_b > 0:
            value = value_a // value_b
            self.registers[op_a] = value
            # advance the progself.ram counter
            #self.PC += 3
        else:
            print("Unable to divide by zero")
            self.stop = True

    def op_hlt(self, op_a, op_b):
        print("STOP NOW!HLT:PC:", self.PC)
        self.stop = True

    def op_ldi(self, op_a, op_b):
        self.registers[op_a] = op_b
    
    def op_jne(self, op_a, op_b):
        # If `E` flag is clear (false, 0), jump to the address stored in the given register.   
        test = self.FL << 5
        if self.FL == 100 or self.FL == 10:
            register = ram[self.PC + 1]       
            value = self.registers[register]
            self.PC = value 
        else:
            self.PC += 2   

    def op_jeq(self, op_a, op_b):
        test = self.FL << 5
        # If `equal` flag is set (true), jump to the address stored in the given register.   
        if self.FL == 1:
            register = self.ram[self.PC + 1]
            value = self.registers[register]
            self.PC = value 
        # if the values are not equal advance the program counter
        else:
            self.PC += 2     
        
    def op_jmp(self, op_a, op_b):
        #pass # not finished with this
        address_to_jump_to = self.ram[op_a]
        self.registers[op_a] = address_to_jump_to
        self.PC = address_to_jump_to              

    def op_ld(self, op_a, op_b):
        self.registers[op_a] = self.registers[op_b]

    def op_inc(self, op_a, op_b):
        value = self.ram[op_a] + 1
        self.registers[op_a] = value

    def op_mod(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        # make sure we arent trying to divide by zero
        if value_b > 0:
            value = value_a // value_b
            self.registers[op_a] = value
            # advance the progself.ram counter
            self.PC += 3
        else:
            print("Unable to divide by zero")
            running = False    

    def op_mul(self, op_a, op_b):
        prod = (self.registers[op_a] * self.registers[op_b])
        self.registers[op_a] = prod
          
    def op_not(self, op_a, op_b):
        value_a = self.registers[op_a]
        value = ~value_a
        self.registers[op_a] = value

    def op_push(self, op_a, op_b):
        self.registers[7] = ( self.registers[7] - 1 ) % 255
        self.SP = self.registers[7]
        value = self.registers[op_a]
        self.ram[self.SP] = value              

    def op_pop(self, op_a, op_b):
        self.SP = self.registers[7]
        value = self.ram[self.SP]
        register_address = self.ram[self.PC + 1]
        self.registers[register_address] = value
        self.registers[7] = ( self.SP + 1 ) % 255

    def op_ret(self, op_a, op_b):
        # get the location of our return_to_address
        self.SP = self.registers[7]
        # save the address from the stack
        address_to_return_to = self.ram[self.SP]
        # update thestack pointer
        self.registers[7] = ( self.SP + 1 ) % 255
        # set the program counter to its new location address
        self.PC = address_to_return_to

    def op_pra(self, op_a, op_b):
        pass
        print("PRA:PC:", self.PC)
        # read the register number
        print("self.registers[op_a]:", self.registers[op_a])
        print("self.ram[op_a]:", self.ram[op_a])
        value_a = bin(self.ram[op_a])
        value_a = str(value_a)
        print("value_a:", value_a)     
        x = self.text_from_bits(value_a)
        self.PC += 2

    def op_prn(self, op_a, op_b):
        print(self.registers[op_a])

    def op_or(self, op_a, op_b):
        # Perform a bitwise-OR between the values in registerA and registerB, storing the
        # result in registerA.
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        value = value_a | value_b
        self.registers[op_a] = value

    def op_xor(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        value = value_a ^ value_b
        self.registers[op_a] = value
    
    def op_shl(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        value = value_a << value_b
        self.registers[op_a] = value

    def op_shr(self, op_a, op_b):
        value_a = self.registers[op_a]
        value_b = self.registers[op_b]
        value = value_a >> value_b
        self.registers[op_a] = value

    def op_st(self, op_a, op_b):
        # store the value in register b in the address stored in register a
        # get the two register addresses from the PC
         self.registers[op_a] = self.registers[op_b] 
 
    def op_sub(self, op_a, op_b):
        first_register = self.ram[self.PC + 1]
        second_register = self.ram[self.PC + 2]
        diff = self.registers[first_register] - self.registers[second_register]
        self.registers[op_a] = diff

    def ram_read(self, mar):
        return self.ram[mar]
      
    def ram_write(self, mar, mdr): 
        self.ram[mar] = mdr

    ''' 
    This is the utilities section
    '''
    # RETURNS A 8BIT BINARY
    def p8(self, v):
        return "{:08b}".format(v)

    def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    def int2bytes(i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

    # use this to print letters
    def get_ascii(self, binary_in):
 
        print("binary_in: ", binary_in)
        n = int(str(binary_in))
        n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return n
    ''' 
    End of utilities 
    '''
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
        
        self.registers[7] = 255
 
        # Main Loop
        while not self.stop:

            # *********************************
            #
            # these are for debugging
            #
            # self.trace()
            # self.print_registers()
            # print("ram:", self.ram)
            #
            # End of debugging
            #
            # *********************************

            self.IR = self.ram_read(self.PC)
            op_a = self.ram_read(self.PC + 1)
            op_b = self.ram_read(self.PC + 2)
                 
            self.op_size = self.IR >> 6
            self.ins_set = ((self.IR >> 4) & 0b1) == 1
            
            if not self.ins_set:
                self.PC += self.op_size + 1

            if self.IR in self.ops:
                self.ops[self.IR](op_a, op_b)
              
        sys.exit 


