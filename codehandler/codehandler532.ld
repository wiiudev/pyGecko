OUTPUT(build/codehandler532.elf);

SECTIONS {
	.text 0x011dd000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 532);

PROVIDE(DCFlushRange = 0x1023ee8);
PROVIDE(memset = 0x1035a54);
PROVIDE(memcpy = 0x1035a68);
PROVIDE(__gh_errno_ptr = 0x1040308);
PROVIDE(OSCreateThread = 0x10414c8);
PROVIDE(OSResumeThread = 0x10419b0);
PROVIDE(socket_lib_init = 0x10c02f4);
PROVIDE(accept = 0x10c054c);
PROVIDE(bind = 0x10c06cc);
PROVIDE(listen = 0x10c09cc);
PROVIDE(recv = 0x10c0aec);
PROVIDE(send = 0x10c16ac);
PROVIDE(socket = 0x10c21c8);
PROVIDE(socketclose = 0x10c2314);
PROVIDE(GX2WaitForVsync = 0x1151964);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x1004e9c0);
PROVIDE(entry_point = 0x1005d180);
PROVIDE(MEMAllocFromDefaultHeap = 0x100b4878);
PROVIDE(MEMFreeToDefaultHeap = 0x100b487c);
PROVIDE(OSDynLoad_FindExport = 0x102b790);
PROVIDE(OSDynLoad_Acquire = 0x102a31c);