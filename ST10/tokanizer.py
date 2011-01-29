import sys
import re
import parser

keyword = ['class', 'constructor', 'function', 'method', 
            'field', 'static', 'var', 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', 'let', 'do',
            'if', 'else', 'while', 'return']
symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~' ]
token_list_count = 0
final_list = []
pgm_list = []

def next_token_temp():
    global token_list_count
    tkn = pgm_list[token_list_count]
    token = (tkn, token_type(tkn))
    return token

def next_token():
    global token_list_count
    token = pgm_list[token_list_count]
    token_list_count += 1
    token = (token, token_type(token))
    return token
        
def token_type(token):
    for ch in keyword:
        if ch == token:
            return 'keyword'
    for ch in symbol:
        if ch == token:
            #if token == '<':
            #print_token('&lt;', 'symbol')
            return 'symbol'
        #else:
                #print_token(token, 'symbol')
                #return
    if token.isdigit():
        return 'integerConstant'
    if token.isalpha() or token[0] ==  '_' or token.isalnum():
        return 'identifier'
    else:
        return 'stringConstant'

def final_list_preparation(val):
    list2 = []
    string_l = []
    string_constant = ""
    i = -1
    for value in val:
        if value == '\r':
            continue
        else:
            if value == "\"" and i!=0:
                i=0
                continue
            if i == 0 and value == "\"":
                i = 2
                pgm_list.append(string_constant)
                string_constant = ''
                continue
            if i == 0:
                string_constant = string_constant + ' ' + value
                continue
            else:
                pgm_list.append(value)

def tokanizer(file_path):
    f = open(file_path, 'r')
    lines = f.readlines()
    for ch in lines:
        final_list.append(re.findall("\s*(\d+|\w+|.)", ch))
    for ch in final_list:
        final_list_preparation(ch)
		

