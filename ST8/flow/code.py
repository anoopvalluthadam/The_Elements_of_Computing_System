
import parser

label_num = 0 #Global label number

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
        push_static(parser.FILENAME, insn.arg2)
       
def pop_insn_to_asm(insn):
    if insn.arg1 in ('local', 'argument', 'this', 'that'):
        pop_local_arg_this_that(insn.arg1, insn.arg2)
    elif insn.arg1 in ('pointer', 'temp'):
        pop_pointer_temp(insn.arg1, insn.arg2)
    elif insn.arg1 == 'static':
        pop_static(parser.FILENAME, insn.arg2)

def label_insn_to_asm(insn):
    print '(' + insn.arg1 + ')'

def goto_insn_to_asm(insn):
    print '@' + insn.arg1
    print '0;JMP'

def if_insn_to_asm(insn):
    a = ('@SP',
         'AM=M-1',
         'D=M',
         '@'+insn.arg1,
         'D;JNE')
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

def codegen(filename):
    g = parser.parse(filename)
    for insn in g:
        insn_to_asm(insn)

if __name__ == '__main__':
    import sys
    codegen(sys.argv[1])

       

