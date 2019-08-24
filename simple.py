import sys
​
PRINT_TIM    = 1
HALT         = 2
PRINT_NUM    = 3
PRINT_SUM    = 4
SAVE         = 5
ADD          = 6
​
ram = [0] * 256
registers = [0] * 8 # [0, 0, 0, 0, 0, 0, 0, 0]
SP = registers[7] # STACK POINTER (SP) R7
IS = registers[6] # INTERRUPT STATUS (IS) R6
IM = registers[5] # INTERRUPT MASK (IM) R5

PC = 0
FL = 0
running = True
​
​
def load_memory():
    address = 0
    try:
        with open(sys.argv[1]) as file:
            for line in file:
                comment_split = line.split('#')
                possible_number = comment_split[0]
​
                if possible_number == '' or possible_number == '\n':
                    continue
                instruction = int( possible_number[0:8], base=2)
                ram[address] = instruction
                address += 1
​
    except IOError:  #FileNotFoundError
        print('I cannot find that file, check the name')
        sys.exit(2)
​
​
load_memory()
​


while running:
    command = ram[PC]
​
    if command == PRINT_TIM:
        print('Tim!')
        PC += 1
​
    elif command == PRINT_NUM:
        num = ram[PC + 1]
        print(num)
        PC += 2
​
    elif command == PRINT_SUM:
        first_number = ram[PC + 1]
        second_number = ram[PC + 2]
        print(first_number + second_number)
        PC += 3
​
    elif command == SAVE:
        register = ram[PC + 1]
        number_to_save = ram[PC + 2]
        registers[register] = number_to_save
        PC += 3
​
    elif command == ADD:
        first_register = ram[PC + 1]
        second_register = ram[PC + 2]
        sum = registers[first_register] + registers[second_register]
        registers[first_register] = sum
        PC += 3
​
    elif command == HALT:
        running = False
​
    else:
        print('command not recognized: {}'.format(command))
        running = False