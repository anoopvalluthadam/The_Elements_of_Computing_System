#command parsing module
import codemd

class parse_command:
    
    def __init__(self, file_name):
        f = open(file_name, 'r')
        commands = f.read()
        commands = commands.split('\r\n')
        for command in commands:
            cmd_type = command_type(command)
            if cmd_type == 'C_PUSH':
                self.arg1, self.arg2 = push_or_pop_command_extract(command)
                codemd.code_writer(self.arg1, self.arg2, cmd_type)
            if cmd_type == 'C_POP':
                self.arg1,self.arg2 = push_or_pop_command_extract(command)
                codemd.code_writer(self.arg1, self.arg2, cmd_type)
            if cmd_type == 'C_ARITHMETIC':
                codemd.code_writer(command, 'C_ARITHMETIC', cmd_type)       
         
#push command Extracting
def push_or_pop_command_extract(command):
    splited_command = command.split(' ')
    return splited_command[1], splited_command[2]

#command type CHecking
def command_type(command):
    splited_command = command.split(' ')
    if splited_command[0] == 'push':
        return 'C_PUSH'
    if splited_command[0] == 'pop':
        return 'C_POP'
    if splited_command[0] == 'add' or splited_command[0] == 'eq' or splited_command[0] == 'gt' or splited_command[0] == 'lt' or splited_command[0] == 'sub' or splited_command[0] == 'neg' or splited_command[0] == 'and' or splited_command[0] == 'or' or splited_command[0] == 'not':
        return 'C_ARITHMETIC'

p=parse_command("/media/CY83RK1D/Documents/ZWS/Projects/The_Elements_of_Computing_System/ST7/project07/BasicTest.vm")
