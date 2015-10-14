OUTPUT(build/codehandler532.elf);

SECTIONS {
	.text 0x011DD000 : {
		*(.text._start);
		*(.text*);
	}
	/DISCARD/ : {
		*(*);
	}
}

PROVIDE(ver = 532);

PROVIDE(DCFlushRange = 0x01023EE8);
PROVIDE(memset = 0x01035A54);
PROVIDE(memcpy = 0x01035A68);
PROVIDE(__gh_errno_ptr = 0x01040308);
PROVIDE(OSCreateThread = 0x010414C8);
PROVIDE(OSResumeThread = 0x010419B0);
PROVIDE(socket_lib_init = 0x010C02F4);
PROVIDE(accept = 0x010C054C);
PROVIDE(bind = 0x010C06CC);
PROVIDE(listen = 0x010C09CC);
PROVIDE(recv = 0x010C0AEC);
PROVIDE(send = 0x010C16AC);
PROVIDE(socket = 0x010C21C8);
PROVIDE(socketclose = 0x010C2314);
PROVIDE(GX2WaitForVsync = 0x01151964);
PROVIDE(entry_point = 0x1005D180);
PROVIDE(MEMAllocFromDefaultHeapEx = 0x1004E9C0);
PROVIDE(MEMAllocFromDefaultHeap = 0x100B4878);
PROVIDE(MEMFreeToDefaultHeap = 0x100B487C);
PROVIDE(OSDynLoad_FindExport = 0x0102B790);
PROVIDE(OSDynLoad_Acquire = 0x0102A31C);
