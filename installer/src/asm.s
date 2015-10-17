
.section .asmstart

.extern _main
.globl _start
_start:
	# Load a good stack
	lis 1,0x1AB5
	ori 1,1,0xD138
	# Go!
	b _main
