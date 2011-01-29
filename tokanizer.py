import sys
import re
import parser

token_list_count = 0
final_list = []
pgm_list = []

def next_token(tokanized_pgm):
    global token_list_count
    token = tokanized_pgm[token_list_count]
    token_list_count += 1
    return token

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
    #parser.parsing(pgm_list)
    print pgm_list

file_path = sys.argv[1]
tokanizer(file_path)
