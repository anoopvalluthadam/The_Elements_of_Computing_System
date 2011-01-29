#Code Writing Module
label_count = 0
#File opend for code Writing
f = open('BasicTest.asm', 'a')

#Code Writer Function
def code_writer(arg1, arg2, cmd_type):
    if cmd_type == 'C_PUSH':
        push_code_writer(arg1, arg2)
    if cmd_type == 'C_POP':
        pop_code_writer(arg1, arg2)
    if cmd_type == 'C_ARITHMETIC':
        if arg1 == 'add' or arg1 == 'sub' or arg1 == 'and' or arg1 == 'or':
            add_code_writer(arg1)
        if arg1 == 'eq' or arg1 == 'gt' or arg1 == 'lt':
            label_code_writer(arg1)
        if arg1 == 'neg':
            neg_code_writer(arg1)

#Generate assembly code for Neg
def neg_code_writer(arg1):
    f.write('@SP\n')
    f.write('M=M-1\n')
    f.write('A=M\n')
    if arg1 == 'not':
        f.write('D=!M\n')
    if arg1 == 'neg':
        f.write('D=-M\n')
    f.write('M=D\n')
    f.write('@SP\n')
    f.write('M=M+1\n')
    f.write('\n')
    f.write('//----------------negation------------------\n')

#Generate assembly code for eq
def label_code_writer(arg1):
    global label_count
    count = str(label_count)
    label_count +=1
    f.write('@SP\n')
    f.write('M=M-1\n')
    f.write('A=M\n')
    f.write('D=M\n')
    f.write('@SP\n')
    f.write('M=M-1\n')
    f.write('A=M\n')
    f.write('D=M-D\n')
    f.write('@JUMP')
    f.write(count)
    f.write('\n')
    if arg1 == 'eq':
        f.write('D;JEQ\n')
    if arg1 == 'gt':
        f.write('D;JGT\n')
    if arg1 == 'lt':
        f.write('D;JLT\n')
    f.write('@SP\n')
    f.write('A=M\n')    
    f.write('M=0\n')
    f.write('@CONTINUE')
    f.write(count)
    f.write('\n')
    f.write('0;JMP\n')
    f.write('(JUMP')
    f.write(count)
    f.write(')\n')
    f.write('@SP\n')
    f.write('A=M\n')
    f.write('M=-1\n')
    f.write('(CONTINUE')
    f.write(count)
    f.write(')\n')
    f.write('@SP\n')
    f.write('M=M+1\n')
    f.write('//------Label Code Writer------------------\n')

#Generate Assembly code for Push command
def push_code_writer(arg1, arg2):
    if arg1 == 'argument' or arg1 == 'local' or arg1 == 'this' or arg1 == 'that' or arg1 == 'temp':
        push_segment_code_writer(arg1, arg2)
    else:
        f.write('@')
        f.write(arg2)
        f.write('\n')
        f.write('D=A\n')
        f.write('@SP\n')    
        f.write('A=M\n')
        f.write('M=D\n')
        f.write('@SP\n')
        f.write('M=M+1\n')
        f.write('//--------PUSH Constant---------------\n')

#Generate Assembly code for Add Command
def add_code_writer(arg1):
    f.write('@SP\n')
    f.write('M=M-1\n')
    f.write('A=M\n')
    f.write('D=M\n')
    f.write('@SP\n')
    f.write('A=M\n')
    f.write('A=A-1\n')
    if arg1 == 'add':
        f.write('D=D+M\n')
    if arg1 == 'sub':
        f.write('D=M-D\n')
    if arg1 == 'and':
        f.write('D=D&M\n')
    if arg1 == 'or':
        f.write('D=D|M\n')
    f.write('M=D\n')
    f.write('//---------ADD-------------\n')

#Generate assembly code for Push command according to segment
def push_segment_code_writer(arg1, arg2):
    f.write('@')
    f.write(arg2)
    f.write('\n')
    f.write('D=A\n')
    if arg1 == 'argument':
        f.write('@ARG')
    if arg1 == 'local':
        f.write('@LCL\n')
    if arg1 == 'this':
        f.write('@THIS\n')
    if arg1 == 'that':
        f.write('@THAT\n')
    if arg1 == 'temp':
        f.write('R5\n')
    f.write('D=D+M\n')
    f.write('A=D\n')
    f.write('D=M\n')
    f.write('@SP\n')
    f.write('A=M\n')
    f.write('M=D\n')
    f.write('@SP\n')
    f.write('M=M+1\n')
    f.write('//-------------Push Segmnet -----------------------------\n')    
        
#Generate Code for POP command according to segment
def pop_code_writer(arg1, arg2):
    f.write('@')
    f.write(arg2)
    f.write('\n')
    f.write('D=A\n')
    if arg1 == 'argument':
        f.write('@ARG\n')
    if arg1 == 'local':
        f.write('@LCL\n')
    if arg1 == 'this':
        f.write('@THIS\n')
    if arg1 == 'that':
        f.write('@THAT\n')
    if arg1 == 'temp':
        f.write('@R5\n')
    f.write('D=D+M\n')
    f.write('@24576\n')
    f.write('M=D\n')
    f.write('@SP\n')
    f.write('A=M\n')
    f.write('M=D\n')
    f.write('@24576\n')
    f.write('A=M\n')
    f.write('M=D\n')
    f.write('@SP\n')
    f.write('M=M-1\n')
    f.write('//--------------------POP According to Segment\n')


