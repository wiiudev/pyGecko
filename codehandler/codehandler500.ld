OUTPUT(build/codehandler500.elf);

SECTIONS {
	.text 0x011DBC00 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 500);

PROVIDE(DCFlushRange = 0x01023A00);
PROVIDE(memset = 0x0103544C);
PROVIDE(memcpy = 0x01035460);
PROVIDE(__gh_errno_ptr = 0x0103F2CC);
PROVIDE(OSCreateThread = 0x01040480);
PROVIDE(OSResumeThread = 0x01040968);
PROVIDE(socket_lib_init = 0x010BF2F4);
PROVIDE(accept = 0x010BF54C);
PROVIDE(bind = 0x010BF6CC);
PROVIDE(listen = 0x010BF9CC);
PROVIDE(recv = 0x010BFAEC);
PROVIDE(send = 0x010C06AC);
PROVIDE(socket = 0x010C11C8);
PROVIDE(socketclose = 0x010C1314);
PROVIDE(GX2WaitForVsync = 0x01150868);
PROVIDE(entry_point = 0x1005CB00);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x1004E2D0);
PROVIDE(MEMAllocFromDefaultHeap = 0x100B41F8);
PROVIDE(MEMFreeToDefaultHeap = 0x100B41FC);
PROVIDE(OSDynLoad_FindExport = 0x0102B3E4);
PROVIDE(OSDynLoad_Acquire = 0x01029CD8);
