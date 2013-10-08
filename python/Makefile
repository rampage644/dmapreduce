ARCH=x86_64-nacl

CC=${ARCH}-gcc
AR=${ARCH}-ar
CXX=${ARCH}-g++
RANLIB=${ARCH}-ranlib

CFLAGS=-Wall -Wno-long-long -msse4.1 -m64

ZVM_PREFIX_ABSPATH = $(abspath $(ZVM_PREFIX))
ZEROVM=${ZVM_PREFIX_ABSPATH}/bin/zerovm -QPs


CFLAGS+=-std=c99 -g


LDFLAGS=-L/home/zvm/git/zpython2 -lpython2.7 -lbz2 -lz -lutil -lmapreduce -lnetworking -lrt -lm -lsqlite3

CFLAGS+=-I/home/zvm/git/zpython2/install/include/python2.7 -I//home/zvm/git/zpython2/Modules

all: clean createdirs map.nexe reduce.nexe
	./gendatamanifest.sh

map.nexe: obj/map.o obj/user_implem.o
	$(CC) -o $@ $? $(LDFLAGS)

reduce.nexe: obj/reduce.o obj/user_implem.o
	$(CC) -o $@ $? $(LDFLAGS)

obj/map.o: src/map.c
	$(CC) -c -o $@ $< ${CFLAGS} 

obj/reduce.o: src/reduce.c
	$(CC) -c -o $@ $< ${CFLAGS}

obj/user_implem.o: src/user_implem.c
	$(CC) -c -o $@ ${CFLAGS} $< -D_GNU_SOURCE

createdirs:
	chmod u+rwx genmanifest.sh start.sh
	@mkdir -p obj

clean: 
	@rm -fr obj/
	@rm -f *.nexe
	@rm -f nameservice.log
 


