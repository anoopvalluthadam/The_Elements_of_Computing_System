keyword = ['class', 'constructor', 'function', 'method', 
            'field', 'static', 'var', 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', 'let', 'do',
            'if', 'else', 'while', 'return']
symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~' ]
op = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~' ]
statements_list = ['let', 'if', 'else', 'while', 'do', 'return']
keyword_constant = ['true', 'false', 'null', 'this']
token_list_count = 0
token = ''

def token_type_and_print(token):
    t_type = token_type(token)
    print_token(token, t_type)

def next_token(tokanized_pgm):
    global token_list_count
    token = tokanized_pgm[token_list_count]
    token_list_count += 1
    return token
    
def class_name_type(className):
    if token_type(className) == 'identifier':
        return 'identifier'

def print_token(token, type):
    if token == '<':
        token = '&lt;'
    print '<' + type +'>' + ' ' +token + ' ' + '</'+ type + '>', token_list_count

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

def subroutine_call_checking(token, tokanized_pgm):
#Subroutine name Checking
    global token_list_count
    t_type = token_type(token)
    if t_type == 'identifier':
        next_tkn = next_token(tokanized_pgm)
        token_list_count -= 1
        if next_tkn == '(' or next_tkn == '.':
            #token_list_count -= 1
            return 'subroutineCall'

def parsing(tokanized_pgm):
#Parsing according to Jack Gramer
        token = next_token(tokanized_pgm)
        print '===============class============', token
        t_type = token_type(token)
        if token == 'class':
           class_method(token, tokanized_pgm)

def class_method(token, tokanized_pgm):
    print '<class>'
    t_type = token_type(token)
    print_token(token, t_type)
    className = next_token(tokanized_pgm)
    class_n_type = class_name_type(className)
    if class_n_type == 'identifier':
        print_token(className, 'identifier')
    token = next_token(tokanized_pgm)
    if token == '{':
        token_type_and_print(token)
        token = class_body(token, tokanized_pgm)
    if token == '}':
        token_type_and_print(token)
    print '</class>'  

def class_body(token, tokanized_pgm):
#Body of a class Method
    token = next_token(tokanized_pgm)
    if token == 'static' or token == 'field':
        while token == 'static' or token == 'field':
            token_type_and_print(token)
            token = class_var_dec(token, tokanized_pgm)
            token = next_token(tokanized_pgm)
    if token == 'constructor' or token == 'function' or token == 'method' or token == 'void':
        while token == 'constructor' or token == 'function' or token == 'method' or token == 'void':
            token = subroutine_dec(token, tokanized_pgm)
            token = next_token(tokanized_pgm)
    return token

def class_var_dec(token, tokanized_pgm):
#Class variable Declaration, Grammer: ('static' | 'field' ) type varName (',' varName)* ';'
    print '<classVarDec>'
    token_type_and_print(token)
    
    print '</classVarDec>'
    return token
    
def subroutine_dec(token, tokanized_pgm):
#Subroutine Declaration, Grammer: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    print '<subroutineDec>'
    if token == 'constructor' or token == 'function' or token == 'method':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token == 'void' or token == basic_type(token):
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            t_type = token_type(token)
            if t_type == 'identifier':
                print_token(token, t_type)
                token = next_token(tokanized_pgm)
                if token == '(':
                    token_type_and_print(token)
                    token = next_token(tokanized_pgm)
                if token != ')':
                    token = parameter_list(tokanized_pgm)
                if token == ')':
                    token_type_and_print(token)
                    token = subroutine_body(tokanized_pgm)
    token = next_token(tokanized_pgm)                
    print '</subroutineDec>'
    return token
    
def basic_type(token):
    if token == 'int' or token == 'char' or token == 'boolean' or class_name_type(token) == 'identifier':
        return token

def parameter_list(tokanized_pgm):
    print '<parameterList>'
    token = next_token(tokanized_pgm)
    while token != ')':
        if token == basic_type(token):
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            if var_name(token) == 'identifier':
                token_type_and_print(token)
                token = next_token(tokanized_pgm)
                if token == ')':
                    break
                if token == ',':
                    token_type_and_print(token)
        token = next_token(tokanized_pgm)
    print '</parameterList>'
    if token == ')':
        token_type_and_print(token)
    token = subroutine_body(tokanized_pgm)
    return token

def var_name(token):
    if token_type(token) == 'identifier':
        return 'identifier'   

def subroutine_body(tokanized_pgm):
    #Subroutine Body, Grammer: '{' varDec* statements '}'
    print '<subroutineBody>'
    token = next_token(tokanized_pgm)
    if token == '{':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        token = inside_subroutine_body(token, tokanized_pgm)
        if token == '}':
            token_type_and_print(token)    
    print '</subroutineBody>'
    return token

def statements(token, tokanized_pgm):
#Check whether the token is a statement ot not, Grammer: statement*
    print '<statements>'
    while token == 'if' or token == 'while' or token == 'do' or token == 'let' or token == 'return':
            token = statement(token, tokanized_pgm)
            print '==========inside subroutine body===============', token
    print '</statements>'
    return token        
    
def inside_subroutine_body(token, tokanized_pgm):
    while token == 'var':
        if token == 'var':
            token = var_dec(token, tokanized_pgm)
            token = next_token(tokanized_pgm)
    if token != 'var':
        token = statements(token, tokanized_pgm)
        #token = next_token(tokanized_pgm)
    return token

def var_dec(token,tokanized_pgm):
#Variable Declaration Method,Grammer: 'var' type varName (',' varName)* ';'
    print '<varDec>'
    token_type_and_print(token)
    token = next_token(tokanized_pgm)
    if token == basic_type(token):
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        var_dec_token_type(token)
        token = next_token(tokanized_pgm)
        while token != ';':
            if token == ',':
                token_type_and_print(token)
                token = next_token(tokanized_pgm)
                var_dec_token_type(token)
            token = next_token(tokanized_pgm)
        if token == ';':
            token_type_and_print(token)
    print '</varDec>'
    return token

def var_dec_token_type(token):
#Checking of token type in variable declaration method (var_dec)
    t_type = token_type(token)
    if t_type == 'identifier':
        token_type_and_print(token)

def statement(token, tokanized_pgm):
#Statements like let if while etc
    global token_list_count
    print '<statement>'
    if token == 'let':
        token = let_statement(token, tokanized_pgm)
    if token == 'if':
        token = if_statement(token, tokanized_pgm)
    if token == 'while':
        token = while_statement(token, tokanized_pgm)
    if token == 'do':
        token = do_statement(token, tokanized_pgm)
    if token == 'return':
        token = return_statement(token, tokanized_pgm)
    print '</statement>'
    print '$$$$$$$$$$$$$$$$$$$$$$$$$', token_list_count
    if token == ';':
        token = next_token(tokanized_pgm)
    print '======================statement==============', token
    return token

def let_statement(token, tokanized_pgm):
#let statemetns operations, Grammer: 'let' varName ('[' expression ']')? '=' expression ';'
    print '<letStatement>'
    global token_list_count
    token_type_and_print(token)
    token = next_token(tokanized_pgm)
    if token_type(token) == 'identifier':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token == '[':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            token = expression(token, tokanized_pgm)
            token = let_statement_inner_part(token, tokanized_pgm)  
        if token == '=':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            token = expression(token, tokanized_pgm)
            print '========================after calling expressiom , after = ========================', token
            if token == ';':
                token_type_and_print(token)
                print '************************************', token
            else:
                print '++++++++++++++++'
                token = next_token(tokanized_pgm)
                if token == ';':
                    token_type_and_print(token)
    print '</letStatement>', token, token_list_count
    token = next_token(tokanized_pgm)
    print '==========================', token, token_list_count
    return token

def let_statement_inner_part(token, tokanized_pgm):
#Let statement innerpart, calling experssion if any occerence found
    token = next_token(tokanized_pgm)
    if token == ']':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
    return token

def if_statement(token, tokanized_pgm):
#if statement, Grammer: 'if' '(' expression ')' '{' statement '}'
    print '<ifStatement>'
    token = next_token(tokanized_pgm)
    if token == '(':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token != ')':
            token = next_token(tokanized_pgm)
            token = expression(token)
        elif token == ')':
            token = if_statement_inner_part(token)
    print '</ifStatement>'
    return token

def if_statement_inner_part(token, tokanized_pgm):
#if statement inner part 
    token_type_and_print(token)
    token = next_token(tokanized_pgm)
    if token == '{':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token != '}':
            satement(token, tokanized_pgm)
        if token == '}':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
        if token == 'else':
            if token == '{':
                token_type_and_print(token)
                token = next_token(tokanized_pgm)
            if token != '}':
                statements(token, tokanized_pgm)
            if token == '}':
                token_type_and_print(token)
    return token

def while_statement(token, tokanized_pgm):
#While tatement, Grammer: 'while' '(' expression ')' '{' statements  '}'
    print '<whileStatement>'
    if token == 'while':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token == '(':
            token_type_and_print(token)
            token = while_statement_inner_part(token, tokanized_pgm)
    print '</whileStatement>'
    return token

def while_statement_inner_part(token, tokanized_pgm):
#While statement inner part
    token = next_token(tokanized_pgm)
    if token != ')':
        token = expression(token, tokanized_pgm)
    if token == ')':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token == '{':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            if token != '}':
                token = statements(token, tokanized_pgm)
            if token == '}':
                token_type_and_print(token)
    return token

def do_statement(token, tokanized_pgm):
#do statement, Grammer: 'do' subroutineCall ';'
    print '<doStatement>'
    token_type_and_print(token)
    token = subroutine_call(token, tokanized_pgm)
    token = next_token(tokanized_pgm)
    if token == ';':
        token_type_and_print(token)
    print '</doStatement>'
    return token

def return_statement(token, tokanized_pgm):
#return statement, Grammer: 'return' expession? ';'
    print '<returnSatement>'
    token_type_and_print(token)
    token = next_token(tokanized_pgm)
    if token != ';':
        token = next_token(tokanized_pgm)
        token = expression(toknen, tokanized_pgm)
    if token == ';':
        token_type_and_print(token)
    print '</returnStatement>'
    return token

def expression(token,tokanized_pgm):
#Expressions, Grammer: term (op term)*
    print '<expressions>'
    global token_list_count
    token = term(token, tokanized_pgm)
    token = next_token(tokanized_pgm)
    t_type_o = op_checking(token)
    if t_type_o == 'op':
        while t_type_o == 'op':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            token = term(token, tokanized_pgm)
            token = next_token(tokanized_pgm)
            t_type_o = op_checking(token)
    else:
        token_list_count -= 1
        token = tokanized_pgm[token_list_count]
    print '</expressions>', token
    return token

def op_checking(token):
#Operator Checking
    for ch in op:
        if ch == token:
            return 'op'

def term(token, tokanized_pgm):
#term, Grammer: integerConstant | stringConstant | keywordConstant | 
#varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    global token_list_count
    print '<term>'
    t_type = token_type(token)
    if t_type == 'integerConstant' or t_type == 'stringConstant':
        print_token(token, t_type) 
        print token_list_count
    if t_type == 'identifier':
        temp = token_list_count
        temp_token = tokanized_pgm[temp]
        if temp_token != '.' and temp_token != '(' and temp_token != '[':
            print_token(token, t_type)  
            #token_list_count -= 1  
    t_type = keyword_constant_checking(token)
    if t_type == 'keywordConstant':
        print_token(token, t_type)
    t_type = var_name_expression(token, tokanized_pgm)
    if t_type == 'varnameExpression':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token == '[':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            if token != ']':
                token = expression(token, tokanized_pgm)
                token = next_token(tokanized_pgm)
            if token == ']':
                token_type_and_print(token)                
    t_type = subroutine_call_checking(token, tokanized_pgm)          
    if t_type == 'subroutineCall':
        subroutine_call(token, tokanized_pgm)
    if token == '(':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token != ')':
            token = expression(token, tokanized_pgm)
            token = next_token(tokanized_pgm)
        if token == ')':
            token_type_and_print(token)        
    if token == '~' or term == '-':
        print_token(token, 'unaryOp')
        token = next_token(tokanized_pgm)
        term(token, tokanized_pgm)      
    print '</term>', token, token_list_count
    return token
    
def keyword_constant_checking(token):
#Checking whether the token is keyword constant or not
    for ch in keyword_constant:
        if ch == token:
            return 'keywordConstant'

def var_name_expression(token, tokanized_pgm):
#check varName '[' expression ']'
    global token_list_count
    if token_type(token) == 'identifier':
        token2 = next_token(tokanized_pgm)
        token_list_count -= 1
        if token2 == '[':
            return 'varnameExpression'
        
def subroutine_call(token, tokanized_pgm):
#Subroutine call,Grammer: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    print '<subroutineCall>'
    t_type = token_type(token)
    if t_type == 'identifier':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        token = subroutine_call_body(token, tokanized_pgm)
        if token == '.':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
            if token_type(token) == 'identifier':
                token_type_and_print(token)
                token = next_token(tokanized_pgm)
                token = subroutine_call_body(token, tokanized_pgm)
    
    print '</subroutineCall>'
    return token

def subroutine_call_body(token, tokanized_pgm):
#Subroutine call body
    if token == '(':
        token_type_and_print(token)
        token = next_token(tokanized_pgm)
        if token != ')':
            token = expression_list(token, tokanized_pgm)
        if token == ')':
            token_type_and_print(token)
    return token

def expression_list(token, tokanized_pgm):
#Expression List, Grammer: (expression (',' expression)* )?
    print '<expressionList>'
    token = expression(token, tokanized_pgm)
    token = next_token(tokanized_pgm)
    while token != ')':
        if token == ',':
            token_type_and_print(token)
            token = next_token(tokanized_pgm)
        else:
            token = expression(token, tokanized_pgm)
        token = next_token(tokanized_pgm)
    print '</expressionList>', token
    return token
