root := .
project := $(root)/src
build := $(root)/bin
libs := $(root)/../../libwiiu/bin
www := $(root)/../../www
framework := $(root)/../../framework
AS=powerpc-eabi-as
CC=powerpc-eabi-gcc
CFLAGS=-nostdinc -fno-builtin -c
LDFLAGS=-T $(project)/link.ld -nostartfiles -nostdlib -s
all: clean setup main532 main500 main410 main400 main310 main300 main210 main200
setup:
	mkdir -p $(root)/bin/
main532:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=532 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code532.bin $(libs)/532/draw.o $(build)/*.o
main500:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=500 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code500.bin $(libs)/500/draw.o $(build)/*.o
main410:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=410 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code410.bin $(libs)/410/draw.o $(build)/*.o
main400:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=400 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code400.bin $(libs)/400/draw.o $(build)/*.o
main310:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=400 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code310.bin $(libs)/310/draw.o $(build)/*.o
main300:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=300 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code300.bin $(libs)/300/draw.o $(build)/*.o
main210:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=210 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code210.bin $(libs)/210/draw.o $(build)/*.o
main200:
	$(AS) $(project)/asm.s -o $(root)/asm.o
	$(CC) $(CFLAGS) -DVER=200 $(project)/*.c
	#-Wa,-a,-ad
	mv -f $(root)/*.o $(build)
	$(CC) $(LDFLAGS) -o $(build)/code200.bin $(libs)/200/draw.o $(build)/*.o
clean:
	rm -f -r $(build)/*
