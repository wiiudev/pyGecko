OUTPUT(build/codehandler500.elf);

SECTIONS {
	.text 0x011dbc00 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 500);

PROVIDE(DCFlushRange = 0x1023a00);
PROVIDE(memset = 0x103544c);
PROVIDE(memcpy = 0x1035460);
PROVIDE(__gh_errno_ptr = 0x103f2cc);
PROVIDE(OSCreateThread = 0x1040480);
PROVIDE(OSResumeThread = 0x1040968);
PROVIDE(socket_lib_init = 0x10bf2f4);
PROVIDE(accept = 0x10bf54c);
PROVIDE(bind = 0x10bf6cc);
PROVIDE(listen = 0x10bf9cc);
PROVIDE(recv = 0x10bfaec);
PROVIDE(send = 0x10c06ac);
PROVIDE(socket = 0x10c11c8);
PROVIDE(socketclose = 0x10c1314);
PROVIDE(GX2WaitForVsync = 0x1150868);
PROVIDE(entry_point = 0x1005cb00);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x1004e2d0);
PROVIDE(MEMAllocFromDefaultHeap = 0x100b41f8);
PROVIDE(MEMFreeToDefaultHeap = 0x100b41fc);
PROVIDE(OSDynLoad_FindExport = 0x102b790); /* TODO: Fix these :\ */
PROVIDE(OSDynLoad_Acquire = 0x102a31c); /* TODO: Fix these :\ */

