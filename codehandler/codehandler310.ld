OUTPUT(build/codehandler310.elf);

SECTIONS {
	.text 0x011d3000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 310);

PROVIDE(DCFlushRange = 0x101da3c);
PROVIDE(memset = 0x102b5b0);
PROVIDE(memcpy = 0x102b5c4);
PROVIDE(__gh_errno_ptr = 0x10349dc);
PROVIDE(OSCreateThread = 0x10358b8);
PROVIDE(OSResumeThread = 0x1035d88);
PROVIDE(socket_lib_init = 0x10a7ee0);
PROVIDE(accept = 0x10a80d0);
PROVIDE(bind = 0x10a8250);
PROVIDE(listen = 0x10a8550);
PROVIDE(recv = 0x10a8670);
PROVIDE(send = 0x10a8b98);
PROVIDE(socket = 0x10a93ec);
PROVIDE(socketclose = 0x10a9534);
PROVIDE(GX2WaitForVsync = 0x1142148);
PROVIDE(OSDynLoad_FindExport = 0x1023d88);
PROVIDE(OSDynLoad_Acquire = 0x1022cbc);

PROVIDE(MEMAllocFromDefaultHeapEx = 0x100479AC);
PROVIDE(entry_point = 0x1005BBC0);
PROVIDE(MEMAllocFromDefaultHeap = 0x100A88A0);
PROVIDE(MEMFreeToDefaultHeap = 0x100A88A4);
