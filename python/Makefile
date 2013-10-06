include ./Makefile.env
CFLAGS+=-std=c99 -g


LDFLAGS=-L/home/zvm/git/zpython2 -lpython2.7 -lbz2 -lz -lutil -lmapreduce -lnetworking -lrt -lm -lsqlite3

CFLAGS+=-I/home/zvm/git/zpython2/install/include/python2.7 -I//home/zvm/git/zpython2/Modules

all: clean createdirs map.nexe reduce.nexe gensort
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
	chmod u+rwx gendatamanifest.sh start.sh
	@mkdir -p obj log data

gensort:
	if test ! -d gensort-1.5 ; then \
		tar xf gensort-1.5.tar.gz ;\
	fi
	$(MAKE) -C gensort-1.5
	ln -s gensort-1.5/valsort .
	ln -s gensort-1.5/gensort .

clean: 
	@rm -fr obj/
	@rm -fr log/
	@rm -f *.txt
	@rm -fr data/
	@rm -f manifest/*.manifest	
	@rm -f nvram/*.nvram
	@rm -f *.nexe
	@rm -f nameservice.log
	@rm -fr gensort-1.5/
	@rm valsort gensort 2>/dev/null || true 


