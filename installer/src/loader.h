#ifndef LOADER_H
#define LOADER_H

#include "../../../libwiiu/src/coreinit.h"
#include "../../../libwiiu/src/draw.h"
#include "../../../libwiiu/src/socket.h"
#include "../../../libwiiu/src/types.h"
#include "../../../libwiiu/src/vpad.h"

/* Kernel address table */
#if VER == 300
	#define KERN_ADDRESS_TBL		0xFFEB66E4
	
	#define KERN_SYSCALL_TBL_1		0xFFE84D50
	#define KERN_SYSCALL_TBL_2		0xFFE85150
	#define KERN_SYSCALL_TBL_3		0xFFE85D50
	#define KERN_SYSCALL_TBL_4		0xFFE85550
	#define KERN_SYSCALL_TBL_5		0xFFE85950
	
	#define KERN_CODE_READ			0xFFF02214
	#define KERN_CODE_WRITE			0xFFF02234
#elif VER == 310
	#define KERN_ADDRESS_TBL		0xFFEB66E4
	
	#define KERN_SYSCALL_TBL_1		0xFFE84D50
	#define KERN_SYSCALL_TBL_2		0xFFE85150
	#define KERN_SYSCALL_TBL_3		0xFFE85D50
	#define KERN_SYSCALL_TBL_4		0xFFE85550
	#define KERN_SYSCALL_TBL_5		0xFFE85950
	
	#define KERN_CODE_READ			0xFFF02214
	#define KERN_CODE_WRITE			0xFFF02234
#elif VER == 400
	#define KERN_ADDRESS_TBL		0xFFEB7E5C
	
	#define KERN_SYSCALL_TBL_1		0xFFE84C90
	#define KERN_SYSCALL_TBL_2		0xFFE85090
	#define KERN_SYSCALL_TBL_3		0xFFE85C90
	#define KERN_SYSCALL_TBL_4		0xFFE85490
	#define KERN_SYSCALL_TBL_5		0xFFE85890
	
	#define KERN_CODE_READ			0xFFF02214
	#define KERN_CODE_WRITE			0xFFF02234
#elif VER == 410
	#define KERN_ADDRESS_TBL		0xFFEB902C
	
	#define KERN_SYSCALL_TBL_1		0xFFE84C90
	#define KERN_SYSCALL_TBL_2		0xFFE85090
	#define KERN_SYSCALL_TBL_3		0xFFE85C90
	#define KERN_SYSCALL_TBL_4		0xFFE85490
	#define KERN_SYSCALL_TBL_5		0xFFE85890
	
	#define KERN_CODE_READ			0xFFF02214
	#define KERN_CODE_WRITE			0xFFF02234
#elif VER == 500
	#define KERN_ADDRESS_TBL		0xFFEA9E4C
	
	#define KERN_SYSCALL_TBL_1		0xFFE84C70
	#define KERN_SYSCALL_TBL_2		0xFFE85070
	#define KERN_SYSCALL_TBL_3		0xFFE85470
	#define KERN_SYSCALL_TBL_4		0xFFEA9120
	#define KERN_SYSCALL_TBL_5		0xFFEA9520
	
	#define KERN_CODE_READ			0xFFF021f4
	#define KERN_CODE_WRITE			0xFFF02214
#elif VER == 532
	#define KERN_ADDRESS_TBL		0xFFEAAA10
	
	#define KERN_SYSCALL_TBL_1		0xFFE84C70
	#define KERN_SYSCALL_TBL_2		0xFFE85070
	#define KERN_SYSCALL_TBL_3		0xFFE85470
	#define KERN_SYSCALL_TBL_4		0xFFEA9CE0
	#define KERN_SYSCALL_TBL_5		0xFFEAA0E0
	
	#define KERN_CODE_READ			0xFFF02274
	#define KERN_CODE_WRITE			0xFFF02294
#elif VER == 550
	#define KERN_ADDRESS_TBL		0xFFEAB7A0
	
	#define KERN_SYSCALL_TBL_1		0xFFE84C70
	#define KERN_SYSCALL_TBL_2		0xFFE85070
	#define KERN_SYSCALL_TBL_3		0xFFE85470
	#define KERN_SYSCALL_TBL_4		0xFFEAAA60
	#define KERN_SYSCALL_TBL_5		0xFFEAAE60
	
	#define KERN_CODE_READ			0xFFF023D4
	#define KERN_CODE_WRITE			0xFFF023F4
#else
#error "Unsupported Wii U software version"
#endif

void _main();
void kern_write(void *addr, uint32_t value);
void* memset(void* dst, const uint8_t val, uint32_t size);
void* memcpy(void* dst, const void* src, uint32_t size);

#endif /* LOADER_H */