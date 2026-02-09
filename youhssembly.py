import sys,time

def clamp(n: int,min_v,max_v):
    return max(min_v, min(n,max_v))

alloc = [0]
mem_tape = [0] * 4096
def YSM(mem: list, acc: list,code: str):
    """
    Runs Youhssembly code through a string. Youhssembly is a limited version of assembly made as a test
    programming language for simulating CPU and RAM relations using Python. Below is a list of every function.
    ```python
    REG(addr,value) -> bin # Registers a given integer value as binary in memory.
    MOV(addr1,addr2) -> bin # Copies the data from a given address to another.
    LDA(value) -> bin # Loads an integer value into the accumulator. The accumulator can be defined through a parameter in the function.
    STA(addr) -> bin # Stores the accumulator's value into an address.
    ADD(addr,value) -> None # Adds an integer to a given address.
    SUB(addr,value) -> None # Subtracts a given address's value by an integer.
    MLT(addr,value) -> None # Multiplies an integer value by the address's value.
    DIV(addr,value) -> None # Divides an integer value by the address's value. Division is rounded DOWN.
    SAY(addr) -> bin # Prints out a byte's value.
    ECHO(any) -> str # Echoes any value.
    CHR(addr) -> chr # Prints out a byte's value.
    WHILE(addr, kw, val) -> None # Perform a while loop for any actions while an addresses obeys a keyword-value statement, such as '<addr> > 0'.
    WHILEND(addr) -> None # End a while loop that utilizes the given address.

    ``` 
    
    :param mem: memory tape. Type must be list.
    :param acc: accumulator byte. Type must be list.
    :param code: code. Type must be string.
    """
    ########
    # const
    ########

    i = 0
    start_time = time.perf_counter()
    split_code = code.split("\n")
    OPCODES = ["REG","MOV","LDA","STA","ADD","MLT","DIV","SAY","ECHO","SUB","CHR","WHILE","WHILEND"]
    KWS = ["GRT","LST","EQL","NEQL","GEQL","SEQL"]
    digits = range(9)
    cond = False
    int_limit = 2 ** 1024
    chr_output = ""

    ########
    # lexer
    ########

    while i < len(split_code):
        if i < len(split_code):
            line_code = split_code[i].split(" ") 
        else:
            ValueError("incorrect code format")
        line_params = line_code[1:]
        line_inst = line_code[0]
        def check_cond():
            if line_params[1] == "GRT":
                return int(mem[int(line_params[0])]) > int(line_params[2])
                
            elif line_params[1] == "LST":
                return int(mem[int(line_params[0])]) < int(line_params[2])
                
            elif line_params[1] == "EQL":
                return int(mem[int(line_params[0])]) == int(line_params[2])
                
            elif line_params[1] == "NEQL":
                return int(mem[int(line_params[0])]) != int(line_params[2])
                
            elif line_params[1] == "GEQL":
                return int(mem[int(line_params[0])]) >= int(line_params[2])
                    
            elif line_params[1] == "SEQL":
                return int(mem[int(line_params[0])]) <= int(line_params[2])

            else:
                raise ValueError("Incorrect WHILE condition")
                

        
        if line_inst in OPCODES:
            for param in line_params:
                if param not in KWS:
                    if len(param) > 0:
                        if param[0] == "$" and not param == "$ACC":
                            if line_inst != "STA" or line_inst != "LDA":
                                line_params[line_params.index(param)] = mem[int(param[1:])]
                        elif param == "$ACC":
                            line_params[line_params.index(param)] = acc[0]
                        else:
                            if param[1:] in digits:
                                param = int(param)
            if line_inst == "REG":
                # REG <addr> <value> | :param addr -- 0 <= <addr> < len(tape) | :param value -- 0 <= <value> <= int_limit
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] = int(line_params[1])
            
            if line_inst == "MOV":
                # MOV <addr_sender> <addr_receiver> | mem[addr_receiver] = mem[addr_sender]
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= len(mem):
                    mem[int(line_params[1])] = mem[int(line_params[0])]
            
            if line_inst == "LDA":
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= int_limit:
                    acc[0] = line_params[0]
            
            if line_inst == "STA":
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
            
                    mem[int(line_params[0])] = int(acc[0])
            if line_inst == "ADD":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit: # if valid byte and enough params
                    mem[int(line_params[0])] += int(line_params[1])
            
            if line_inst == "MLT":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit: # if valid byte and enough params
                    ad_mem = int(mem[int(line_params[0])])
                    ad_mem *= int(line_params[1])
                    mem[int(line_params[0])] = ad_mem
            
            if line_inst == "DIV":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 1 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] = int(mem[int(line_params[0])] / int(line_params[1]))
            
            if line_inst == "SUB":
                if len(line_params) == 2 and 0 <= int(line_params[0]) <= len(mem) and 0 <= int(line_params[1]) <= int_limit:
                    mem[int(line_params[0])] -= int(line_params[1])
            
            if line_inst == "SAY":
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    print(mem[int(line_params[0])])
            
            if line_inst == "ECHO":
                say = ""
                for kw in line_params:
                    say += (str(kw) + " ")
                print(say)
            
            if line_inst == "CHR":
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    print(chr(mem[line_params[0]]))
            
            if line_inst == "WHILE":
                # WHILE <addr> <kw> <value>
                if len(line_params) == 3 and 0 <= int(line_params[0]) <= len(mem) and line_params[1] in KWS and 0 <= int(line_params[2]) <= int_limit:
                    cond = check_cond()
            
            if line_inst == "WHILEND":
                if len(line_params) == 1 and 0 <= int(line_params[0]) <= len(mem):
                    for line in split_code:
                        if line.split(" ")[0] == "WHILE" and line.split(" ")[1] == line_params[0] and cond == True:
                            i = line.index(line.split(" ")[0])
                        
        
                        
                        


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