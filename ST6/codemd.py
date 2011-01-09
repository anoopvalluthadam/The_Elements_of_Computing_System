vcount = [15]
lcount = [1]
sixt = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
azcomp = {"0" : "101010", "1" : "111111", "-1" : "111010", 
            "D" : "001100", "A" : "110000", "!D" : "001101", "!A" : "110001", 
            "-D" : "001111", "-A" : "110011", "D+1" : "011111", "A+1" : "110111", 
            "D-1" : "001110", "A-1" : "110010", "D+A" : "000010", "D-A" : "010011", 
            "A-D" : "000111", "D&A" : "000000", "D|A" : "010101"}
            
aocomp = {"M" : "110000", "!M" : "110001", "-M" : "110011", "M+1" : "110111",
                    "M-1" : "110010", "D+M" : "000010", "D-M" : "010011", 
                    "M-D" : "000111", "D&M" : "000000", "D|M" : "010101"} 
dest = {"M" : "001", "D" : "010", "MD" : "011", "A" : "100", 
                "AM" : "101", "AD" : "110", "AMD" : "111", "0" : "000"}
jump = {"JGT" : "001", "JEQ" : "010", "JGE" : "011", "JLT" : "100", 
                "JNE" : "101", "JLE" : "110", "JMP" : "111", "0" : "000"}
           
symbols = {"SP" : 0, "LCL" : 1, "ARG" : 2, "THIS" : 3, 
                   "THAT" : 4, "SCREEN" : 16384, "KBD" : 24576, 
                    "R0" : 0, "R1" : 1, "R2" : 2, "R3" : 3, 
                    "R4" : 4, "R5" : 5, "R6" : 6, "R7" : 7, "R8" : 8, 
                    "R9" : 9, "R10" : 10, "R11" : 11, "R12" : 12, 
                    "R13" : 13, "R14" : 14, "R15" : 15}

loop = {}
variable = {}

def init_sixt():
    sixt [0 :] = '0000000000000000'  


def jump_command(list):
    for ch in jump:
        if ch == list[1]:
            sixt[13 : ] = jump[list[1]]
 
def dest_value(list):
   
    for ch in dest:
        if ch == list[0]:
            sixt[10 : 13] = dest[list[0]]
            


def a_value_checking(zcomp, list, ocomp):
    for ch in zcomp:
        if ch == list:
            binary_generation(list, a='0')
    for ch in ocomp:        
        if ch == list:
            binary_generation(list,a='1')
    
               

def convert_binary(str, command, count,vfcount):

    if vfcount == 0:
        make_symboltable(str, command, count)
    else:
        make_binary(str, command, count)


def make_symboltable(str, command, count):      
    
    if str == "L_COMMAND":
        lp = command[1 : -1]    
        loop[lp] = count - lcount[-1]
        lcount.append(lcount[-1]+1)

def make_binary(str, command, count):
    #print command
    flag = 0
    list = []
    zcomp = []
    zcomp = azcomp.keys()    
    ocomp = aocomp.keys()
    scommand1 = []
    scommand2 = []
    if str == "C_COMMAND":
        scommand1 = command.split('=')
        scommand2 = command.split(';')
        if len(scommand2) == 1:        
            a_value_checking(zcomp, scommand1[1], ocomp)
            dest_value(scommand1)
            sixt[13:  ] = '000' 
        if len(scommand1) == 1:
            #print list
            jump_command(scommand2)
            sixt [10 : 13] = '000'
            sixt[3] = '0'
            a_value_checking(zcomp,scommand2[0],ocomp)
            
        to_file()
    if str == "A_COMMAND":
        integer = command.split('@')
        if integer[1].isdigit():
            value=int(integer[1])
            convert_int_to_bin(value)
        else:
            for ch in symbols:
                if ch == integer[1]:
                    flag = 1
                    convert_int_to_bin(symbols[integer[1]]) 
                    return
            if flag == 0:
                for ch in loop:
                    if integer[1] == ch:
                        convert_int_to_bin(loop[integer[1]])
                        flag = 2
                        return 
            if flag == 0:
                #print '========>',variable
                if len(variable) == 0:
                    variable_add(integer[1])
                else:
                    for ch in variable:
                        #print "===========>ch-",ch,"========>integer[1]",integer[1] 
                        if ch == integer[1]:
                            flag == 3
                            convert_int_to_bin(variable[integer[1]])
                            return 
                    if flag == 0:
                            #print "==================>variable add<======================"
                            variable_add(integer[1])   
def binary_generation(ch, a):
    if a == '0':
        bcomp = azcomp[ch]
        combine_binary(bcomp, a)
    if a == '1':
        bcomp = aocomp[ch]
        combine_binary(bcomp,a)


def combine_binary(bcomp, a):
    length = len(bcomp)
    sixt[0] = '1'
    sixt[3] = a
    sixt[1 : 3] = '11'
    sixt[4 : 10] = bcomp      


def dest_command(jlist):
    for ch in dest:
        if ch == jlist[0]:
            sixt[10 : 13] = dest[jlist[0]]        
    
def to_file():
    list = []
    list = ''.join(sixt)
    print list
def convert_int_to_bin(line):
    init_sixt()
    n = line
    bstr = ''
    while n > 0:
	    bstr = str(n % 2) + bstr
	    n = n >> 1
    list = []
    for k in sixt:
        list.append(k)
    length = len(bstr)
    leng = 16 - length 
    list [leng :] = bstr
    s = ''
    string = s.join(list)
    print string

def variable_add(var):
    flag = 1
    if flag == 1:
        variable[var] = vcount[-1] + 1
        vcount.append(variable[var])
        convert_int_to_bin(variable[var])
        #print vcount


