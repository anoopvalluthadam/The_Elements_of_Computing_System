""" Parses vm commads into `insns' """

import re
import os

current_filename = ''

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

class Instruction:
    def __init__(self, type, arg1=None, arg2=None):
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2

def print_insn(insn):
    print 'type = %d, arg1 = %s, arg2 = %s' % (insn.type, insn.arg1, insn.arg2)

def strip_whitespace_comment(line):
    t = re.sub('//.*', '', line)
    return t.strip()
 
def parse_command(cmd):
    a = 'add sub neg eq gt lt and or not'.split()
    t = cmd.split()
    if t[0] in a:
        return Instruction(C_ARITHMETIC, arg1=t[0])
    elif t[0] == 'push':
        return Instruction(C_PUSH, arg1=t[1], arg2=t[2])
    elif t[0] == 'pop':
        return Instruction(C_POP, arg1=t[1], arg2=t[2])
    elif t[0] == 'label':
        return Instruction(C_LABEL, arg1=t[1])
    elif t[0] == 'goto':
        return Instruction(C_GOTO, arg1=t[1])
    elif t[0] == 'if-goto':
        return Instruction(C_IF, arg1=t[1])
    elif t[0] == 'function':
        return Instruction(C_FUNCTION, arg1=t[1], arg2=t[2])
    elif t[0] == 'call':
        return Instruction(C_CALL, arg1=t[1], arg2=t[2])
    elif t[0] == 'return':
        return Instruction(C_RETURN)

def parse(name):
    global current_filename
    if os.path.isdir(name):
        a = os.listdir(name)
        files = filter(lambda x: x[-3:] == '.vm', a)
    else:
        files = [name]
    for filename in files:
        current_filename = filename[0:-3] # strip `.vm' from filename
        lines = open(filename).readlines()
        print '//----------' + filename + '----------'
        for line in lines:
            cmd = strip_whitespace_comment(line)
            if cmd == '': continue
            yield parse_command(cmd)

if __name__ == '__main__':
    import sys
    g = parse(sys.argv[1])
    for insn in g:
        print_insn(insn)
   
