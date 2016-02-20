#include "loader.h"

#define RW_MEM_MAP 0xA0000000
#if VER == 200
	#include "codehandler310.h" //TODO
	#define INSTALL_ADDR  0x011D3000
	#define MAIN_JMP_ADDR 0x0101894C
#elif VER == 210
	#include "codehandler310.h" //TODO
	#define INSTALL_ADDR  0x011D3000
	#define MAIN_JMP_ADDR 0x0101894C
#elif VER == 300
	#include "codehandler310.h" //TODO ???
	#define INSTALL_ADDR  0x011D3000
	#define MAIN_JMP_ADDR 0x0101894C
#elif VER == 310
	#include "codehandler310.h"
	#define INSTALL_ADDR  0x011D3000
	#define MAIN_JMP_ADDR 0x0101894C
#elif VER == 400
	#include "codehandler400.h"
	#define INSTALL_ADDR  0x011DD000
	#define MAIN_JMP_ADDR 0x0101BD4C
#elif VER == 410
	#include "codehandler410.h"
	#define INSTALL_ADDR  0x011DD000
	#define MAIN_JMP_ADDR 0x0101C55C
#elif VER == 500
	#include "codehandler500.h"
	#define INSTALL_ADDR  0x011DD000
	#define MAIN_JMP_ADDR 0x0101C55C
#elif VER == 532
	#include "codehandler532.h"
	#define INSTALL_ADDR  0x011DD000
	#define MAIN_JMP_ADDR 0x0101C55C
#elif VER == 550
	#include "codehandler550.h"
	#define INSTALL_ADDR  0x011DD000
	#define MAIN_JMP_ADDR 0x0101C56C
#endif

#define assert(x) \
	do { \
		if (!(x)) \
			OSFatal("Assertion failed " #x ".\n"); \
	} while (0)

#define ALIGN_BACKWARD(x,align) \
	((typeof(x))(((unsigned int)(x)) & (~(align-1))))

int doBL( unsigned int dst, unsigned int src );
void doOSScreenInit(unsigned int coreinit_handle);
inline void doOSScreenClear();
void doOSScreenPrintPos(char *buf, int pos);
void doVPADWait();

void _main()
{
	/* Get a handle to coreinit.rpl. */
	unsigned int coreinit_handle;
	OSDynLoad_Acquire("coreinit.rpl", &coreinit_handle);

	/* Get for later socket patch */
	unsigned int nsysnet_handle;
	OSDynLoad_Acquire("nsysnet.rpl", &nsysnet_handle);

	/* Get for IP address print */
	unsigned int nn_ac_handle;
	OSDynLoad_Acquire("nn_ac.rpl", &nn_ac_handle);

	/* Load a few useful symbols. */
	void*(*OSEffectiveToPhysical)(const void *);
	void*(*OSAllocFromSystem)(uint32_t size, int align);
	void (*OSFreeToSystem)(void *ptr);
	void (*DCFlushRange)(const void *, int);
	void (*ICInvalidateRange)(const void *, int);
	void (*_Exit)(void) __attribute__ ((noreturn));

	OSDynLoad_FindExport(coreinit_handle, 0, "OSEffectiveToPhysical", &OSEffectiveToPhysical);
	OSDynLoad_FindExport(coreinit_handle, 0, "OSAllocFromSystem", &OSAllocFromSystem);
	OSDynLoad_FindExport(coreinit_handle, 0, "OSFreeToSystem", &OSFreeToSystem);
	OSDynLoad_FindExport(coreinit_handle, 0, "DCFlushRange", &DCFlushRange);
	OSDynLoad_FindExport(coreinit_handle, 0, "ICInvalidateRange", &ICInvalidateRange);
	OSDynLoad_FindExport(coreinit_handle, 0, "_Exit", &_Exit);

	assert(OSEffectiveToPhysical);
	assert(OSAllocFromSystem);
	assert(OSFreeToSystem);
	assert(DCFlushRange);
	assert(ICInvalidateRange);
	assert(_Exit);

	/* Socket functions */
	unsigned int *socket_lib_finish;
	OSDynLoad_FindExport(nsysnet_handle, 0, "socket_lib_finish", &socket_lib_finish);
	assert(socket_lib_finish);

	/* AC functions */
	int(*ACGetAssignedAddress)(unsigned int *addr);
	OSDynLoad_FindExport(nn_ac_handle, 0, "ACGetAssignedAddress", &ACGetAssignedAddress);
	assert(ACGetAssignedAddress);

	/* IM functions */
	int(*IM_SetDeviceState)(int fd, void *mem, int state, int a, int b);
	int(*IM_Close)(int fd);
	int(*IM_Open)();

	OSDynLoad_FindExport(coreinit_handle, 0, "IM_SetDeviceState", &IM_SetDeviceState);
	OSDynLoad_FindExport(coreinit_handle, 0, "IM_Close", &IM_Close);
	OSDynLoad_FindExport(coreinit_handle, 0, "IM_Open", &IM_Open);

	assert(IM_SetDeviceState);
	assert(IM_Close);
	assert(IM_Open);

	/* Restart system to get lib access */
	int fd = IM_Open();
	void *mem = OSAllocFromSystem(0x100, 64);
	memset(mem, 0, 0x100);

	/* set restart flag to force quit browser */
	IM_SetDeviceState(fd, mem, 3, 0, 0);
	IM_Close(fd);
	OSFreeToSystem(mem);

	/* wait a bit for browser end */
	unsigned int t1 = 0x1FFFFFFF;
	while(t1--) ;

	doOSScreenInit(coreinit_handle);
	doOSScreenClear();
	doOSScreenPrintPos("TCPGecko Installer", 0);

	/* Make sure the kernel exploit has been run */
	if (OSEffectiveToPhysical((void *)0xA0000000) == (void *)0)
	{
		doOSScreenPrintPos("You must execute the kernel exploit before installing TCPGecko.", 1);
		doOSScreenPrintPos("Returning to the home menu...",2);
		t1 = 0x3FFFFFFF;
		while(t1--) ;
		doOSScreenClear();
		_Exit();
	}
	else
	{
		doOSScreenPrintPos("Trying to install TCPGecko...", 1);

		/* Our main writable area */
		unsigned int physWriteLoc = (unsigned int)OSEffectiveToPhysical((void*)RW_MEM_MAP);

		/* Install codehandler */
		unsigned int phys_codehandler_loc = (unsigned int)OSEffectiveToPhysical((void*)INSTALL_ADDR);
		void *codehandler_loc = (unsigned int*)(RW_MEM_MAP + (phys_codehandler_loc - physWriteLoc));

		memcpy(codehandler_loc, codehandler_text_bin, codehandler_text_bin_len);
		DCFlushRange(codehandler_loc, codehandler_text_bin_len);
		ICInvalidateRange(codehandler_loc, codehandler_text_bin_len);

		/* Patch coreinit jump */
		unsigned int phys_main_jmp_loc = (unsigned int)OSEffectiveToPhysical((void*)MAIN_JMP_ADDR);
		unsigned int *main_jmp_loc = (unsigned int*)(RW_MEM_MAP + (phys_main_jmp_loc - physWriteLoc));

		*main_jmp_loc = doBL(INSTALL_ADDR, MAIN_JMP_ADDR);
		DCFlushRange(ALIGN_BACKWARD(main_jmp_loc, 32), 0x20);
		ICInvalidateRange(ALIGN_BACKWARD(main_jmp_loc, 32), 0x20);

		/* Patch Socket Function */
		unsigned int phys_socket_loc = (unsigned int)OSEffectiveToPhysical(socket_lib_finish);
		unsigned int *socket_loc = (unsigned int*)(RW_MEM_MAP + (phys_socket_loc - physWriteLoc));

		socket_loc[0] = 0x38600000;
		socket_loc[1] = 0x4E800020;
		DCFlushRange(ALIGN_BACKWARD(socket_loc, 32), 0x40);
		ICInvalidateRange(ALIGN_BACKWARD(socket_loc, 32), 0x40);

		/* The fix for Splatoon and such */
		kern_write((void*)(KERN_ADDRESS_TBL + (0x12 * 4)), 0x00000000);
		kern_write((void*)(KERN_ADDRESS_TBL + (0x13 * 4)), 0x14000000);

		/* All good! */
		unsigned int addr;
		ACGetAssignedAddress(&addr);
		char buf[64];
		__os_snprintf(buf,64,"Success! Your Gecko IP is %i.%i.%i.%i.", (addr>>24)&0xFF,(addr>>16)&0xFF,(addr>>8)&0xFF,addr&0xFF);
		doOSScreenPrintPos(buf, 2);

		doOSScreenPrintPos("Press any button to return to the home menu.", 3);
		doVPADWait();
	}
	doOSScreenClear();
	_Exit();
}

int doBL( unsigned int dst, unsigned int src )
{
	unsigned int newval = (dst - src);
	newval &= 0x03FFFFFC;
	newval |= 0x48000001;
	return newval;
}


/* for internal and gcc usage */
void* memset(void* dst, const uint8_t val, uint32_t size)
{
	uint32_t i;
	for (i = 0; i < size; i++)
		((uint8_t*) dst)[i] = val;
	return dst;
}

void* memcpy(void* dst, const void* src, uint32_t size)
{
	uint32_t i;
	for (i = 0; i < size; i++)
		((uint8_t*) dst)[i] = ((const uint8_t*) src)[i];
	return dst;
}

/* Write a 32-bit word with kernel permissions */
void kern_write(void *addr, uint32_t value)
{
	asm(
		"li 3,1\n"
		"li 4,0\n"
		"mr 5,%1\n"
		"li 6,0\n"
		"li 7,0\n"
		"lis 8,1\n"
		"mr 9,%0\n"
		"mr %1,1\n"
		"li 0,0x3500\n"
		"sc\n"
		"nop\n"
		"mr 1,%1\n"
		:
		:	"r"(addr), "r"(value)
		:	"memory", "ctr", "lr", "0", "3", "4", "5", "6", "7", "8", "9", "10",
			"11", "12"
		);
}

/* OSScreen helper functions */
void doOSScreenInit(unsigned int coreinit_handle)
{
	/* OSScreen functions */
	void(*OSScreenInit)();
	unsigned int(*OSScreenGetBufferSizeEx)(unsigned int bufferNum);
	unsigned int(*OSScreenSetBufferEx)(unsigned int bufferNum, void * addr);

	OSDynLoad_FindExport(coreinit_handle, 0, "OSScreenInit", &OSScreenInit);
	OSDynLoad_FindExport(coreinit_handle, 0, "OSScreenGetBufferSizeEx", &OSScreenGetBufferSizeEx);
	OSDynLoad_FindExport(coreinit_handle, 0, "OSScreenSetBufferEx", &OSScreenSetBufferEx);

	assert(OSScreenInit);
	assert(OSScreenGetBufferSizeEx);
	assert(OSScreenSetBufferEx);

	/* Call the Screen initilzation function */
	OSScreenInit();

	/* Grab the buffer size for each screen (TV and gamepad) */
	int buf0_size = OSScreenGetBufferSizeEx(0);
	int buf1_size = OSScreenGetBufferSizeEx(1);

	/* Set the buffer area */
	OSScreenSetBufferEx(0, (void *)0xF4000000);
	OSScreenSetBufferEx(1, (void *)0xF4000000 + buf0_size);
}

inline void doOSScreenClear()
{
	/* Clear both framebuffers */
	int ii;
	for (ii = 0; ii < 2; ii++)
	{
		fillScreen(0,0,0,0);
		flipBuffers();
	}
}

void doOSScreenPrintPos(char *buf, int pos)
{
	int i;
	for(i=0;i<2;i++)
	{
		drawString(0,pos,buf);
		flipBuffers();
	}
}

void doVPADWait()
{
	unsigned int vpad_handle;
	OSDynLoad_Acquire("vpad.rpl", &vpad_handle);

	/* VPAD functions */
	int(*VPADRead)(int controller, VPADData *buffer, unsigned int num, int *error);
	OSDynLoad_FindExport(vpad_handle, 0, "VPADRead", &VPADRead);
	assert(VPADRead);

	int error;
	VPADData vpad_data;

	/* Read initial vpad status */
	VPADRead(0, &vpad_data, 1, &error);
	while(1)
	{
		VPADRead(0, &vpad_data, 1, &error);
		if(vpad_data.btn_hold)
			break;
	}
}
