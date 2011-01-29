import tokanizer
import sys

keyword_constant = ['true', 'false', 'null', 'this']
op = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~' ]

def basic_type(token):
    if token[0] == 'int' or token[0] == 'char' or token[0] == 'boolean' or tokanizer.token_type(token[0]) == 'identifier':
        return token[0]

def print_token(token, t_type):
#print token
    if token == '<':
        token = '&lt;'
    print '<' + t_type +'>' + ' ' +token + ' ' + '</'+ t_type + '>'

def class_method():
#Class Declaration, Grammer:  'class' className '{' classVarDec* subroutineDec* '}'
    print '<class>'
    token = tokanizer.next_token()
    if token[0] == 'class':
        print_token(token[0], token[1])
    token = tokanizer.next_token()
    if token[1] == 'identifier':
        print_token(token[0], token[1])
    token = tokanizer.next_token()
    if token[0] == '{':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = class_body(token)
    if token[0] == '}':
        print_token(token[0], token[1])
    print '</class>'  

def class_body(token):
#Body of a class Method
    if token[0] == 'static' or token[0] == 'field':
        """while token[0] == 'static' or token[0] == 'field':
            print_token(token[0], token[1])
            token = class_var_dec(token, tokanized_pgm)
            token = next_token(tokanized_pgm)"""
    if token[0] == 'constructor' or token[0] == 'function' or token[0] == 'method' or token[0] == 'void':
        while token[0] == 'constructor' or token[0] == 'function' or token[0] == 'method' or token[0] == 'void':
            token = subroutine_dec(token)
            token = tokanizer.next_token()
    return token

def subroutine_dec(token):
#Subroutine Declaration, Grammer: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    print '<subroutineDec>'
    if token[0] == 'constructor' or token[0] == 'function' or token[0] == 'method':
        print_token(token[0],token[1])
        token = tokanizer.next_token()
        if token[0] == 'void' or token[0] == basic_type(token):
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            if token[1] == 'identifier':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
                token = subroutine_dec_body(token)
    token = subroutine_body(token)
    print '</subroutineDec>'
    return token

def subroutine_dec_body(token):
#subroutine_dec Body part
    if token[0] == '(':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = parameter_list(token)
    if token[0] == ')':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
	return token

def parameter_list(token):
#Parameter List, Grammer: ( (type varName) (',' type varName)*)?
    print '<parameterList>'
    if token[0] == basic_type(token):
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        if token[1] == 'identifier':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            while token[0] == ',':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
                if token[0] == basic_type(token):
                    print_token(token[0], token[1])
                    token = tokanizer.next_token()
                if token[1] == 'identifier':
                    print_token(token[0], token[1])
                token = tokanizer.next_token()
    print '</parameterList>'
    return token

def subroutine_body(token):
    #Subroutine Body, Grammer: '{' varDec* statements '}'
    print '<subroutineBody>'
    if token[0] == '{':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = inside_subroutine_body(token)
        if token[0] == '}':
            print_token(token[0], token[1])
    print '</subroutineBody>'
    return token

def inside_subroutine_body(token):
    while token[0] == 'var':
        if token[0] == 'var':
            token = var_dec(token)
        token = tokanizer.next_token()
    if token[0] != 'var':
        token = statements(token)
        #token = next_token(tokanized_pgm)
    return token

def var_dec(token):
#Variable Declaration Method,Grammer: 'var' type varName (',' varName)* ';'
    print '<varDec>'
    print_token(token[0], token[1])
    token = tokanizer.next_token()
    if token[0] == basic_type(token) or tokanizer.token_type(token[0]) == 'identifier':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        var_dec_token_type(token)
        token = tokanizer.next_token()
        while token[0] != ';':
            if token[0] == ',':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
                var_dec_token_type(token)
            token = tokanizer.next_token()
        if token[0] == ';':
            print_token(token[0], token[1])
    print '</varDec>'
    return token

def var_dec_token_type(token):
#Checking of token type in variable declaration method (var_dec
    if token[1] == 'identifier':
        print_token(token[0], token[1])
        return token

def statements(token):
#Check whether the token is a statement ot not, Grammer: statement*
    print '<statements>'
    while token[0] == 'if' or token[0] == 'while' or token[0] == 'do' or token[0] == 'let' or token[0] == 'return':
            token = statement(token)
            token = tokanizer.next_token()
    print '</statements>'
    return token        

def statement(token):
#Statements like let if while etc, Grammer: letStatement | ifStatement | whileStatement | doStatement | returnStatement
    global token_list_count
    if token[0] == 'let':
        token = let_statement(token)
    if token[0] == 'if':
        token = if_statement(token)
    if token[0] == 'while':
        token = while_statement(token)
    if token[0] == 'do':
        token = do_statement(token)
    if token[0] == 'return':
        token = return_statement(token)
    return token

def let_statement(token):
#let statemetns operations, Grammer: 'let' varName ('[' expression ']')? '=' expression ';'
    print '<letStatement>'
    print_token(token[0], token[1])
    token = tokanizer.next_token()
    if token[1] == 'identifier':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        if token[0] == '[':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            token = expression(token)
            token = let_statement_inner_part(token)
            token = tokanizer.next_token()
        if token[0] == '=':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            token = expression(token)
            token = tokanizer.next_token()
            if token[0] == ';':
                print_token(token[0], token[1])
    print '</letStatement>'
    return token

def let_statement_inner_part(token):
#Let statement innerpart, calling experssion if any occerence found
    token = tokanizer.next_token()
    if token[0] == ']':
        print_token(token[0], token[1])
    return token

def while_statement(token):
#While tatement, Grammer: 'while' '(' expression ')' '{' statements  '}'
    print '<whileStatement>'
    if token[0] == 'while':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        if token[0] == '(':
            print_token(token[0], token[1])
            token = while_statement_inner_part(token)
    print '</whileStatement>'
    return token

def while_statement_inner_part(token):
#While statement inner part
    token = tokanizer.next_token()
    token = expression(token)
    token = tokanizer.next_token()
    if token[0] == ')':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        if token[0] == '{':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            token = statements(token)
            if token[0] == '}':
                print_token(token[0], token[1])
    return token

def do_statement(token):
#do statement, Grammer: 'do' subroutineCall ';'
    print '<doStatement>'
    print_token(token[0], token[1])
    token = tokanizer.next_token()
    token = subroutine_call(token)
    token = tokanizer.next_token()
    if token[0] == ';':
        print_token(token[0], token[1])
    print '</doStatement>'
    return token

def return_statement(token):
#return statement, Grammer: 'return' expession? ';'
    print '<returnSatement>'
    print_token(token[0], token[1])
    token = tokanizer.next_token()
    if token[0] != ';':
        token = expression(token)
    if token[0] == ';':
        print_token(token[0], token[1])
    print '</returnStatement>'
    return token

def term(token):
#term, Grammer: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    print '<term>'
    if token[1] == 'integerConstant' or token[1] == 'stringConstant':
        print_token(token[0], token[1]) 
    if token[1] == 'identifier':
        tmp_token = tokanizer.next_token_temp()
        if tmp_token[0] != '.' and tmp_token[0] != '(' and tmp_token[0] != '[':
            print_token(token[0], token[1])  
        if tmp_token[0] == '[':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            if token[0] == '[':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
            token = expression(token)
            token = tokanizer.next_token()
            if token[0] == ']':
                print_token(token[0], token[1])
        if tmp_token[0] == '(' or tmp_token[0] == '.':
            """ print_token(token[0], token[1])
            token = tokanizer.next_token()
            print_token(token[0], token[1])
            token = tokanizer.next_token()"""
            token = subroutine_call(token)
    t_type = keyword_constant_checking(token[0])
    if t_type == 'keywordConstant':
        print_token(token[0], token[1])
    if token[0] == '(':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = expression(token)
        token = tokanizer.next_token()
        if token[0] == ')':
            print_token(token[0], token[1])   
    if token[0] == '~' or token[0] == '-':
        print_token(token[0], 'unaryOp')
        token = tokanizer.next_token()
        token = term(token)      
    print '</term>'
    return token
    
def keyword_constant_checking(token):
#Checking whether the token is keyword constant or not
    for ch in keyword_constant:
        if ch == token[0]:
            return 'keywordConstant'

def expression(token):
#Expressions, Grammer: term (op term)*
    print '<expression>'
    token = term(token)
    tmp_tkn = tokanizer.next_token_temp()
    t_type_o = op_checking(tmp_tkn[0])
    if t_type_o == 'op':
        token = tokanizer.next_token() 
        while t_type_o == 'op':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            token = term(token)
            tmp_tkn = tokanizer.next_token_temp()
            t_type_o = op_checking(tmp_tkn)
            if t_type_o == 'op':
                token = tokanizer.next_token()
    print '</expression>'
    return token

def op_checking(token):
#Operator Checking
    for ch in op:
        if ch == token:
            return 'op'

def subroutine_call(token):
#Subroutine call,Grammer: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    if token[1] == 'identifier':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = subroutine_call_body(token)
        if token[0] == '.':
            print_token(token[0], token[1])
            token = tokanizer.next_token()
            if token[1] == 'identifier':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
                token = subroutine_call_body(token)
    return token

def subroutine_call_body(token):
#Subroutine call body
    if token[0] == '(':
        print_token(token[0], token[1])
        token = tokanizer.next_token()
        token = expression_list(token)
        if token[0] != ')':
            token = tokanizer.next_token()
        if token[0] == ')':
            print_token(token[0], token[1])
            #token = tokanizer.next_token()
    return token

def expression_list(token):
#Expression List, Grammer: (expression (',' expression)* )?
    print '<expressionList>'
    if token[0] != ')':
        token = expression(token)
        tmp_tkn = tokanizer.next_token_temp()
        if tmp_tkn[0] == ',':
            token = tokanizer.next_token()
            while token[0] == ',':
                print_token(token[0], token[1])
                token = tokanizer.next_token()
                token = expression(token)
                token = tokanizer.next_token() 
    print '</expressionList>'
    return token


file_path = sys.argv[1]
tokanizer.tokanizer(file_path)
class_method()

