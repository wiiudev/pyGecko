OUTPUT(build/codehandler310.elf);

SECTIONS {
	.text 0x011D3000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 310);

PROVIDE(DCFlushRange = 0x0101DA3C);
PROVIDE(memset = 0x0102B5B0);
PROVIDE(memcpy = 0x0102B5C4);
PROVIDE(__gh_errno_ptr = 0x010349DC);
PROVIDE(OSCreateThread = 0x010358B8);
PROVIDE(OSResumeThread = 0x01035D88);
PROVIDE(socket_lib_init = 0x010A7EE0);
PROVIDE(accept = 0x010A80D0);
PROVIDE(bind = 0x010A8250);
PROVIDE(listen = 0x010A8550);
PROVIDE(recv = 0x010A8670);
PROVIDE(send = 0x010A8B98);
PROVIDE(socket = 0x010A93EC);
PROVIDE(socketclose = 0x010A9534);
PROVIDE(GX2WaitForVsync = 0x01142148);
PROVIDE(entry_point = 0x1005BBC0);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x100479AC);
PROVIDE(MEMAllocFromDefaultHeap = 0x100A88A0);
PROVIDE(MEMFreeToDefaultHeap = 0x100A88A4);
PROVIDE(OSDynLoad_FindExport = 0x01023D88);
PROVIDE(OSDynLoad_Acquire = 0x01022CBC);
