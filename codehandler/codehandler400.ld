OUTPUT(build/codehandler400.elf);

SECTIONS {
	.text 0x011DD000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 400);

PROVIDE(DCFlushRange = 0x01020EAC);
PROVIDE(memset = 0x01030E84);
PROVIDE(memcpy = 0x01030E98);
PROVIDE(__gh_errno_ptr = 0x0103A434);
PROVIDE(OSCreateThread = 0x0103B5D0);
PROVIDE(OSResumeThread = 0x0103BAB4);
PROVIDE(socket_lib_init = 0x010B44D4);
PROVIDE(accept = 0x010B4720);
PROVIDE(bind = 0x010B48A0);
PROVIDE(listen = 0x010B4BA0);
PROVIDE(connect = 0x010B49FC);
PROVIDE(recv = 0x010B4CC0);
PROVIDE(send = 0x010B5528);
PROVIDE(socket = 0x010B5DA0);
PROVIDE(socketclose = 0x010B5EEC);
PROVIDE(GX2WaitForVsync = 0x011454BC);
PROVIDE(entry_point = 0x1005A600);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x10049C1C);
PROVIDE(MEMAllocFromDefaultHeap = 0x100AD928);
PROVIDE(MEMFreeToDefaultHeap = 0x100AD92C);
PROVIDE(OSDynLoad_FindExport = 0x01028460);
PROVIDE(OSDynLoad_Acquire = 0x01026E60);
