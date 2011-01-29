
import parser

label_num = 0 #Global label number
current_function = ''

def print_all_cmds(a):
    for cmd in a:
        print cmd

def push_dreg():
    a = ('@SP',
         'A=M',
         'M=D',
         '@SP',
         'M=M+1')
    print_all_cmds(a)

def push_content_of(reg):
    """ Push content of LCL, ARG, THIS or THAT"""
    print '@' + reg
    print 'D=M'
    push_dreg()

def pop_into_star_r13():
    """Pop from top-of-stack to location pointed to by R13"""

    a = ('@SP',
         'AM=M-1',
         'D=M',
         '@R13',
         'A=M',
         'M=D')
    print_all_cmds(a)

def push_constant(const):
    print '@' + const
    print 'D=A'
    push_dreg()

def push_local_arg_this_that(segment, index):
    t = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
    segment = t[segment]
    a = ('@' + segment,
         'D=M',
         '@' + index,
         'A=D+A',
         'D=M')
    print_all_cmds(a)
    push_dreg()

def push_pointer_temp(segment, index):
    t = {'pointer':'3', 'temp':'5'}
    segment = t[segment]
    a = ('@' + segment,
         'D=A',
         '@' + index,
         'A=D+A',
         'D=M')
    print_all_cmds(a)
    push_dreg()

def push_static(filename, index):
    print '@' + filename + '.' + str(index)
    print 'D=M'
    push_dreg()

def pop_local_arg_this_that(segment, index):
    t = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
    segment = t[segment]
    a = ('@' + segment,
         'D=M',
         '@' + str(index),
         'D=D+A',
         '@R13',
         'M=D')  
    print_all_cmds(a)
    pop_into_star_r13()

def pop_pointer_temp(segment, index):
    t = {'pointer':'3', 'temp':'5'}
    segment = t[segment]
    a = ('@' + segment,
         'D=A',
         '@' + index,
         'D=D+A',
         '@R13',
         'M=D')
    print_all_cmds(a)
    pop_into_star_r13()

def pop_static(filename, index):
    a = ('@SP',
         'AM=M-1',
         'D=M',
         '@' + filename + '.' + index,
         'M=D')
    print_all_cmds(a)

def binary_arithmetic_bitwise(op):
    """Generate asm code for add, sub, and, or"""

    t = {'add':'+', 'sub':'-', 'and':'&', 'or':'|'}
    op = t[op]   
    a = ('@SP',
         'AM=M-1',
         'D=M',
         'A=A-1',
         'M=M' + op + 'D')
    print_all_cmds(a)
 
def unary_not_neg(op):
    """Generate as code for not, neg"""

    t = {'not':'!', 'neg':'-'}
    op = t[op]
       
    a = ('@SP',
         'A=M-1',
         'M=' + op + 'M')
    print_all_cmds(a)

def binary_eq_lt_gt(op):
    global label_num
    t = {'eq':'JEQ', 'lt':'JLT', 'gt':'JGT'}
    op = t[op]
    a = ('@SP',
         'AM=M-1',
         'D=M',
         'A=A-1',
         'D=M-D',
         'M=-1',
         '@LABEL' + str(label_num),
         'D;' + op,
         '@SP',
         'A=M-1',
         'M=0',
         '(LABEL' + str(label_num) + ')')
    print_all_cmds(a)
    label_num = label_num + 1

def arith_insn_to_asm(insn):
    if insn.arg1 in ('add', 'sub', 'and', 'or'):
        binary_arithmetic_bitwise(insn.arg1)
    elif insn.arg1 in ('not', 'neg'):
        unary_not_neg(insn.arg1)
    elif insn.arg1 in ('eq', 'lt', 'gt'):
        binary_eq_lt_gt(insn.arg1)

def push_insn_to_asm(insn):
    if insn.arg1 == 'constant':
        push_constant(insn.arg2)
    elif insn.arg1 in ('local', 'argument', 'this', 'that'):
        push_local_arg_this_that(insn.arg1, insn.arg2)
    elif insn.arg1 in ('pointer', 'temp'):
        push_pointer_temp(insn.arg1, insn.arg2)
    elif insn.arg1 == 'static':
        push_static(parser.current_filename, insn.arg2)
       
def pop_insn_to_asm(insn):
    if insn.arg1 in ('local', 'argument', 'this', 'that'):
        pop_local_arg_this_that(insn.arg1, insn.arg2)
    elif insn.arg1 in ('pointer', 'temp'):
        pop_pointer_temp(insn.arg1, insn.arg2)
    elif insn.arg1 == 'static':
        pop_static(parser.current_filename, insn.arg2)

def label_insn_to_asm(insn):
    global current_function
    print '(' + current_function + '$' + insn.arg1 + ')'

def goto_insn_to_asm(insn):
    global current_function
    print '@' + current_function + '$' + insn.arg1
    print '0;JMP'

def if_insn_to_asm(insn):
    a = ('@SP',
         'AM=M-1',
         'D=M',
         '@' + current_function + '$' + insn.arg1,
         'D;JNE')
    print_all_cmds(a)

def function_insn_to_asm(insn):
    global current_function
    current_function = insn.arg1
    print '(' + insn.arg1 + ')'
    for i in range(int(insn.arg2)):
        push_constant('0')

def call_insn_to_asm(insn):
    global label_num
    ret_label = 'RET_ADDR' + str(label_num)
    label_num = label_num + 1
    
    # Push return address
    print '@' + ret_label
    print 'D=A'
    push_dreg();
    
    # Push LCL, ARG, THIS, THAT
    for reg in ('LCL', 'ARG', 'THIS', 'THAT'):
        push_content_of(reg)
    
    # ARG = SP - n - 5
    k = int(insn.arg2) + 5
    print '@SP\n', 'D=M'
    print '@' + str(k) + '\n', 'D=D-A'
    print '@ARG\n', 'M=D'

    # LCL = SP
    print '@SP\n', 'D=M\n', '@LCL\n', 'M=D'

    # goto f
    print '@' + insn.arg1
    print '0;JMP'

    # Generate return address label
    print '(' + ret_label + ')'     

def restore_reg(to,  index):
    """Perform this operation: to = *(FRAME - index)"""

    FRAME = 'R13'
    a = ('@'+FRAME, 'D=M', '@'+str(index), 'A=D-A', 'D=M',
         '@'+to, 'M=D')
    print_all_cmds(a)

def return_insn_to_asm(insn):
    FRAME = 'R13'
    RET = 'R14'

    print '// Function Epilogue'
    # FRAME = LCL
    a = ('@LCL',    'D=M',
         '@'+FRAME, 'M=D')
    print_all_cmds(a)

    # RET = *(FRAME - 5)
    a = ('@'+FRAME, 'D=M',
         '@5',      'A=D-A', 'D=M',
         '@'+RET,   'M=D')
    print_all_cmds(a)

    # *ARG = pop()
    a = ('@SP',  'AM=M-1', 'D=M',
         '@ARG', 'A=M', 'M=D')
    print_all_cmds(a)
   
    # SP = ARG + 1
    a = ('@ARG', 'D=M+1', '@SP', 'M=D')
    print_all_cmds(a)

    # THAT = *(FRAME - 1), THIS = *(FRAME - 2), 
    # ARG = *(FRAME - 3), LCL = *(FRAME - 4)
    for x in enumerate(('THAT', 'THIS', 'ARG', 'LCL')):
        to, index = x[1], x[0]+1
        restore_reg(to, index)
        
    # goto RET
    a = ('@' + RET, 'A=M', '0;JMP')
    print_all_cmds(a)

def insn_to_asm(insn):
    if insn.type == parser.C_ARITHMETIC:
        arith_insn_to_asm(insn)
    elif insn.type == parser.C_PUSH:
        push_insn_to_asm(insn)
    elif insn.type == parser.C_POP:
        pop_insn_to_asm(insn)
    elif insn.type == parser.C_LABEL:
        label_insn_to_asm(insn)
    elif insn.type == parser.C_GOTO:
        goto_insn_to_asm(insn)
    elif insn.type == parser.C_IF:
        if_insn_to_asm(insn)
    elif insn.type == parser.C_FUNCTION:
        function_insn_to_asm(insn)
    elif insn.type == parser.C_CALL:
        call_insn_to_asm(insn)
    elif insn.type == parser.C_RETURN:
        return_insn_to_asm(insn)

def emit_bootstrap_code():
    a = ('@256', 'D=A', '@SP', 'M=D')
    print_all_cmds(a)
    
    # call Sys.init 0
    insn_to_asm(parser.Instruction(type=parser.C_CALL, arg1='Sys.init', arg2='0'))    

def codegen(name):
    print '//----------Bootstrap Code----------'
    emit_bootstrap_code()
    g = parser.parse(name)
    for insn in g:
        insn_to_asm(insn)

if __name__ == '__main__':
    import sys
    codegen(sys.argv[1])

