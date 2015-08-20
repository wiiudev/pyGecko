#ifndef LOADER_H
#define LOADER_H

#include "../../../libwiiu/src/coreinit.h"
#include "../../../libwiiu/src/socket.h"
#include "../../../libwiiu/src/types.h"

void _start();

void _entryPoint();

/* Arbitrary kernel write syscall */
void kern_write(void *addr, uint32_t value);

#endif /* LOADER_H */