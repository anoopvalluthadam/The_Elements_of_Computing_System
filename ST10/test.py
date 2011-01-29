import re

expr = "if (b = 2* 3+ a*10)"

print re.findall("\s*(\d+|\w+|.)", expr)
