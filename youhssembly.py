##############################################################
#               YOUHSSEMBLY by YouhWithAnH
# Youhssembly is an open source "high-level low-level"
# esolang that aims to replicate assembly in a virtual
# environment. This language isn't very good, but it's more
# readable than others out there. There are no floats nor
# strings in YSM, only 1024-bit integers. Enjoy! And mind the
# poor optimization.
##############################################################

import sys,time

def clamp(n: int,min_v,max_v):
    return max(min_v, min(n,max_v))

alloc = [0]
mem_tape = [0] * 4096
def YSM(mem: list, acc: list,code: str):
    ########
    # const
    ########

    i = 0
    start_time = time.perf_counter()
    split_code = code.replace("\t","").split("\n")
    OPCODES = ["REG","MOV","LDA","STA","ADD","MLT","DIV","SAY","ECHO","SUB","CHR","WHILE","WHILEND","EXP","READ"] # for the instructions
    KWS = ["EQL","NEQL","GRT","LST","GEQL","LEQL"] # for the conditions
    digits = range(9)
    cond = False
    int_limit = 2 ** 1024

    ########
    # lexer
    ########

    while i < len(split_code):
        if i < len(split_code):
            line_code = split_code[i].split(" ") 
        else:
            ValueError("incorrect code format")
        ii = 0
        while ii < len(line_code): # this is some dumb code that allows for indentation by nullifying all empty parameters (spaces)
            if line_code[ii] == "":
                ii += 1
            else:
                break
        line_params = line_code[1+ii:]
        line_inst = line_code[0+ii]
        def check_cond():
            # this is used for WHILE loops. basically: checks if address number satisfies the condition in relation to an integer value        
            if line_params[1] == "EQL":
                return int(mem[int(line_params[0])]) == int(line_params[2])
            elif line_params[1] == "NEQL":
                return int(mem[int(line_params[0])]) != int(line_params[2])
            elif line_params[1] == "GRT":
                return int(mem[int(line_params[0])]) > int(line_params[2])
            elif line_params[1] == "LST":
                return int(mem[int(line_params[0])]) < int(line_params[2])
            elif line_params[1] == "GEQL":
                return int(mem[int(line_params[0])]) >= int(line_params[2])
            elif line_params[1] == "LEQL":
                return int(mem[int(line_params[0])]) <= int(line_params[2])
            else:
                raise ValueError("Incorrect WHILE condition")
                

        
        if line_inst in OPCODES:
            for param in line_params:
                if param not in KWS:
                    if len(param) > 0:
                        # defines that thing where $<address> = address' value
                        if param[0] == "$" and not param == "$ACC":
                            if line_inst != "STA" or line_inst != "LDA":
                                line_params[line_params.index(param)] = mem[int(param[1:])]
                        elif param == "$ACC":
                            line_params[line_params.index(param)] = acc[0]
                        # similarly, #<address> = length of address' value
                        elif param[0] == "#" and not param == "#ACC":
                            if line_inst != "STA" or line_inst != "LDA":
                                line_params[line_params.index(param)] = len(str(mem[int(param[1:])]))
                        elif param == "#ACC":
                            line_params[line_params.index(param)] = len(str(acc[0]))
                        else:
                            if param[1:] in digits:
                                param = int(param)
            if line_inst == "REG":
                # REG <address> <int_value> -- makes an address = the int value specified
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] = int(line_params[1])
            
            if line_inst == "MOV":
                # MOV <address_1> <address_2> -- makes address_2 = address_1
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= len(mem):
                    mem[int(line_params[1])] = mem[int(line_params[0])]

            if line_inst == "READ":
                # READ <address> -- address = input of the user
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    read = input()
                    if 0 <= int(read) <= int_limit:
                        mem[int(line_params[0])] = int(read)
            
            if line_inst == "LDA":
                # LDA <int_value> -- loads an integer value into the accumulator
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= int_limit:
                    acc[0] = line_params[0]
            
            if line_inst == "STA":
                # STA <address> -- stores the accumulator's value into the specified address
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    mem[int(line_params[0])] = int(acc[0])
            
            ############ ARITHMETIC
                # all arithmetic instructions (ALL OF THEM) follow this form:
                    # INST <address> <int_value>
                # list of instructions and what they mean:
                    # ADD = "+"
                    # MLT = "*"
                    # DIV = "/" (obs: outputs the floor of the division. DIV 0 3 given Reg 0 = 2 is going to be 0)
                    # SUB = "-" (obs: no negative numbers)

            if line_inst == "ADD":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] += int(line_params[1])
            
            if line_inst == "MLT":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    ad_mem = int(mem[int(line_params[0])])
                    ad_mem *= int(line_params[1])
                    mem[int(line_params[0])] = ad_mem
            
            if line_inst == "EXP":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    ad_mem = int(mem[int(line_params[0])])
                    ad_mem **= int(line_params[1])
                    mem[int(line_params[0])] = ad_mem
            
            if line_inst == "DIV":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 1 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] = int(mem[int(line_params[0])] / int(line_params[1]))
            
            if line_inst == "SUB":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] -= int(line_params[1])
            
            if line_inst == "ECHO":
                # ECHO <words> -- always outputs a string. if you use $<addr> for any parameter, it outputs that address's value
                say = ""
                for kw in line_params:
                    say += (str(kw) + " ")
                print(say)
            
            if line_inst == "WHILE":
                # WHILE <address> <condition> <int_value> (see: check_cond() for condition)
                if len(line_params) == 3 and 0 <= int(line_params[0]) <= len(mem) and line_params[1] in KWS and 0 <= int(line_params[2]) <= int_limit:
                    cond = check_cond()
                    p = 0
                    while p < len(split_code):
                        if split_code[p].split(" ")[0] == "WHILEND" and split_code[p].split(" ")[1] == line_params[0] and cond == False:
                            i = p-1
                            break
                        p += 1
            
            if line_inst == "WHILEND":
                # WHILEND <address> -- address must be equal to its WHILE counterpart to end the loop
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    p = 0
                    while p < len(split_code):
                        if split_code[p].split(" ")[0] == "WHILE" and split_code[p].split(" ")[1] == line_params[0] and cond == True:
                            i = p-1
                            break
                        p += 1
        ########
        # formatter
        ########
        j = 0
        while j < len(mem):
            mem[j] = clamp(mem[j],0,int_limit)

            j += 1
        for a in acc:
            a = clamp(int(a),0,int_limit)

        i += 1
    end_time = time.perf_counter()
    elaps = end_time - start_time
    print(f'Elapsed program time: {elaps:0.4f}')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as file:
            YSM(mem_tape,alloc,file.read())
    else:
        print("Usage: python youhssembly.py <file.ysm>")