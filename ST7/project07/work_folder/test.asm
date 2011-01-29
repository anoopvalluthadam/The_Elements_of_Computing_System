@0
D=A //D=10
@LCL //A=1,M=12 suppose
D=D+M //D=22
@24576 //A=6,M=0
M=D //Ram 6 now dolds 22
@SP //A=0,M=256
A=M //A=256 ,M = 890 suppose
M=D
@24576 //A=6,M=22
A=M
M=D
@SP
M=M-1



