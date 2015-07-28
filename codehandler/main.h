/* string.h */
#define NULL ((void *)0)

extern void *memcpy(void *dst, const void *src, int bytes);
extern void *memset(void *dst, int val, int bytes);

/* errno.h */
extern int *__gh_errno_ptr(void);
#define errno (*__gh_errno_ptr())

#define EWOULDBLOCK 6

/* malloc.h */
extern void *(* const MEMAllocFromDefaultHeapEx)(int size, int align);
extern void *(* const MEMAllocFromDefaultHeap)(int size);
extern void *(* const MEMFreeToDefaultHeap)(void *ptr);

#define memalign (*MEMAllocFromDefaultHeapEx)
#define malloc (*MEMAllocFromDefaultHeap)
#define free (*MEMFreeToDefaultHeap)

/* socket.h */
#define AF_INET 2
#define SOCK_STREAM 1
#define IPPROTO_TCP 6

#define MSG_DONTWAIT 32

extern void socket_lib_init();
extern int socket(int domain, int type, int protocol);
extern int socketclose(int socket);
extern int connect(int socket, void *addr, int addrlen);
extern int send(int socket, const void *buffer, int size, int flags);
extern int recv(int socket, void *buffer, int size, int flags);

struct in_addr {
	unsigned int s_addr;
};
struct sockaddr_in {
	short sin_family;
	unsigned short sin_port;
	struct in_addr sin_addr;
	char sin_zero[8];
};

extern int bind(int socket, void *addr, int size);
extern int listen(int socket, int backlog);
extern int accept(int socket, void *addr, int *size);

/* coreinit.rpl */
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
	char tag[8];                     /* 0x000 "OSContxt" */
	int32_t gpr[32];                 /* 0x008 from OSDumpContext */
	uint32_t cr;                     /* 0x088 from OSDumpContext */
	uint32_t lr;                     /* 0x08c from OSDumpContext */
	uint32_t ctr;                    /* 0x090 from context switch code */
	uint32_t xer;                    /* 0x094 from context switch code */
	uint32_t srr0;                   /* 0x098 from OSDumpContext */
	uint32_t srr1;                   /* 0x09c from OSDumpContext */
	char _unknowna0[0xb8 - 0xa0];
	uint64_t fpr[32];                /* 0x0b8 from OSDumpContext */
	int16_t spinLockCount;           /* 0x1b8 from OSDumpContext */
	char _unknown1ba[0x1bc - 0x1ba]; /* 0x1ba could genuinely be padding? */
	uint32_t gqr[8];                 /* 0x1bc from OSDumpContext */
	char _unknown1dc[0x1e0 - 0x1dc];
	uint64_t psf[32];                /* 0x1e0 from OSDumpContext */
	int64_t coretime[3];             /* 0x2e0 from OSDumpContext */
	int64_t starttime;               /* 0x2f8 from OSDumpContext */
	int32_t error;                   /* 0x300 from OSDumpContext */
	char _unknown304[0x6a0 - 0x304];
} OSThread;                          /* 0x6a0 total length from RAM dumps */

extern bool OSCreateThread(OSThread *thread, void (*entry)(int,void*), int argc, void *args, void *stack, size_t stack_size, int32_t priority, int16_t affinity);
extern void OSResumeThread(OSThread *thread);

extern void DCFlushRange(const void *addr, size_t length);

extern int OSDynLoad_Acquire(char* rpl, unsigned int *handle);
extern int OSDynLoad_FindExport(unsigned int handle, int isdata, char *symbol, void *address);

/* gx */
extern void GX2WaitForVsync(void);

/* main */
extern int (* const entry_point)(int argc, char *argv[]);

#define main (*entry_point)

/* BSS section */
struct bss_t {
	int error, line;
	OSThread thread;
	char stack[0x8000];
};