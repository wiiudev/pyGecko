OUTPUT(build/codehandler410.elf);

SECTIONS {
	.text 0x011d9800 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 410);

PROVIDE(DCFlushRange = 0x1020eac);
PROVIDE(memset = 0x1030ed0);
PROVIDE(memcpy = 0x1030ee4);
PROVIDE(__gh_errno_ptr = 0x103a96c);
PROVIDE(OSCreateThread = 0x103bb08);
PROVIDE(OSResumeThread = 0x103bfec);
PROVIDE(socket_lib_init = 0x10b44d4);
PROVIDE(accept = 0x10b4720);
PROVIDE(bind = 0x10b48a0);
PROVIDE(listen = 0x10b4ba0);
PROVIDE(recv = 0x10b4cc0);
PROVIDE(send = 0x10b5528);
PROVIDE(socket = 0x10b5da0);
PROVIDE(socketclose = 0x10b5eec);
PROVIDE(GX2WaitForVsync = 0x11454bc);
PROVIDE(entry_point = 0x1005a8c0);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x10049edc);
PROVIDE(MEMAllocFromDefaultHeap = 0x100adc28);
PROVIDE(MEMFreeToDefaultHeap = 0x100adc2c);
PROVIDE(OSDynLoad_FindExport = 0x102b790); /* TODO: Fix these :\ */
PROVIDE(OSDynLoad_Acquire = 0x102a31c); /* TODO: Fix these :\ */
