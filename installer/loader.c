#include "loader.h"
#include "codehandler532.h"

#define assert(x) \
    do { \
        if (!(x)) \
            OSFatal("Assertion failed " #x ".\n"); \
    } while (0)

void start()
{
    /* Load a good stack */
    asm(
        "lis %r1, 0x1ab5 ;"
        "ori %r1, %r1, 0xd138 ;"
    );

    /* Get a handle to coreinit.rpl. */
    unsigned int coreinit_handle;
    OSDynLoad_Acquire("coreinit.rpl", &coreinit_handle);

    /* Load a few useful symbols. */
	void (*memcpy)(void *dst, const void *src, int bytes);
    void (*_Exit)(void) __attribute__ ((noreturn));
    void (*DCFlushRange)(const void *, int);
    void *(*OSEffectiveToPhysical)(const void *);
    
    OSDynLoad_FindExport(coreinit_handle, 0, "_Exit", &_Exit);
	  OSDynLoad_FindExport(coreinit_handle, 0, "memcpy", &memcpy);
    OSDynLoad_FindExport(coreinit_handle, 0, "DCFlushRange", &DCFlushRange);
    OSDynLoad_FindExport(
        coreinit_handle, 0, "OSEffectiveToPhysical", &OSEffectiveToPhysical);
    
    assert(_Exit);
    assert(DCFlushRange);
    assert(OSEffectiveToPhysical);

    
    /* Make sure the kernel exploit has been run */
    if (OSEffectiveToPhysical((void *)0xa0000000) != (void *)0x31000000)
	{
        OSFatal("You must run ksploit before installing PyGecko.");
    }
	else
	{
        /* Install codehandler */
		memcpy((void*)0xA11dd000, codehandler_text_bin, codehandler_text_bin_len);
      
		/* Patch coreinit */
		*((uint32_t *)0xA101c55c) = 0x481c0aa5;
		*((uint32_t *)0xA10c0404) = 0x38600000;
		*((uint32_t *)0xA10c0408) = 0x4e800020;

        /* The fix for Splatoon and such */
		kern_write(KERN_ADDRESS_TBL + (0x12 * 4), 0x00000000);
		kern_write(KERN_ADDRESS_TBL + (0x13 * 4), 0x14000000);     
    }

    _Exit();
}