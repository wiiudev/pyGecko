OUTPUT(build/codehandler550.elf);

SECTIONS {
	.text 0x011DD000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 550);

PROVIDE(DCFlushRange = 0x01023F88);
PROVIDE(memset = 0x01035FB4);
PROVIDE(memcpy = 0x01035FC8);
PROVIDE(__gh_errno_ptr = 0x01040900);
PROVIDE(OSCreateThread = 0x01041B64);
PROVIDE(OSResumeThread = 0x01042108);
PROVIDE(socket_lib_init = 0x010C02F4);
PROVIDE(accept = 0x010C054C);
PROVIDE(bind = 0x010C06CC);
PROVIDE(listen = 0x010C09CC);
PROVIDE(recv = 0x010C0AEC);
PROVIDE(send = 0x010C16AC);
PROVIDE(socket = 0x010C21C8);
PROVIDE(socketclose = 0x010C2314);
PROVIDE(GX2WaitForVsync = 0x01151964);
PROVIDE(entry_point = 0x1005E040);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x1004F870);
PROVIDE(MEMAllocFromDefaultHeap = 0x100B5738);
PROVIDE(MEMFreeToDefaultHeap = 0x100B573C);
PROVIDE(OSDynLoad_FindExport = 0x0102B828);
PROVIDE(OSDynLoad_Acquire = 0x0102A3B4);
