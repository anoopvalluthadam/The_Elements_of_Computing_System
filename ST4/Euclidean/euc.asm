	@i
	M=0
(SUB)
	@30
	D=M
	@31
	D=D-M
	@SWAPG
	D,JLT
	@END
	D,JEQ
	@i
	M=D
	@31
	D=M
	@30
	M=D
	@i
	D=M
	@31
	M=D
	@SUB
	0,JMP
(SWAPG)
	@30
	D=M
	@i
	M=D
	@31
	D=M
	@30
	M=D
	@i
	D=M
	@31
	M=D
	@SUB
	0,JMP
(END)
	@END
	0,JMP