OUTPUT_ARCH(powerpc:common)
OUTPUT_FORMAT("binary")
ENTRY(_start)

SECTIONS {
	. = 0x01800000;

	.text : { *(.asmstart) *(.text) }
	.rodata : { *(.rodata .rodata.*) }

	/DISCARD/ : {
		*(*);
	}
}