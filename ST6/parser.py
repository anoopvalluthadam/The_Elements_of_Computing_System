#Sourse code parsing

import re
import codemd 

#Module which translate Assembly Mnemonics in to machine code
def remove_whspace(command):
    str = ''
    for ch in command.split():
        str = str + ch
    return str


class  Parser:

    def __init__ (self, file):
        count = 1
        f = open (file, 'rU')
        str = f.read()
        comm = str.split('\n')
        commands = []
        for com in comm:
            if com != '':
                str = remove_whspace(com)
                if str[1] == '/':
                    continue
                else:
                    commands.append(str)
        i = 0
        while i < 2:
            for command in commands:
                str = self.commandtype(command)          
                binary=codemd.convert_binary(str, command, count, i)
                count = count + 1
            i = i + 1
                 
    def commandtype(self, command):
        
        #This helps to find the type of a command
        
        if command[0] == 'A' or command[0] == 'M' or command[0] == 'D' or command[0] == '0':
            return  "C_COMMAND"
        if command[0] == '@':
            return "A_COMMAND"
        if command[0] == '(':
            return "L_COMMAND"
    
p=Parser("Pong.asm")
