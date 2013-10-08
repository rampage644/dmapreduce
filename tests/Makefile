ARCH=x86_64-nacl

CC=${ARCH}-gcc
AR=${ARCH}-ar
CXX=${ARCH}-g++
RANLIB=${ARCH}-ranlib

CFLAGS=-Wall -Wno-long-long -msse4.1 -m64 -std=c99 -g

ZVM_PREFIX_ABSPATH = $(abspath $(ZVM_PREFIX))
ZEROVM=${ZVM_PREFIX_ABSPATH}/bin/zerovm -QPs

LDFLAGS=-L/home/zvm/git/zpython2 -lpython2.7 -lbz2 -lz -lutil -lmapreduce -lnetworking -lrt -lm -lsqlite3
CFLAGS+=-I/home/zvm/git/zpython2/install/include/python2.7 -I/home/zvm/git/zpython2/Modules -I.

NAME=python_test

all: $(NAME).nexe manifest
	$(ZEROVM) $(NAME).manifest
	@cat stdout.$(NAME)
	@echo "=============="
	@cat stderr.$(NAME)

$(NAME).nexe: python.c /home/zvm/git/zpython2/libpython2.7.a
	$(CC) $< -o $@ $(CFLAGS) $(LDFLAGS)

manifest:
	python run.py

clean:
	@rm *.nexe *.o *.conf std* *.log *.manifest >/dev/null 2>&1 || true