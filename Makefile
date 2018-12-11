## BASIC MAKEFILE ##
# General syntax of a Makefile
# target [target ...] : [dependent ...]
#<tab>[command...]


CC = g++
CPPFLAGS = -std=c++11 -pthread -ggdb
#LDFLAGS

#SOURCES = unnamed_pipe.cpp
SOURCES = pipe_from_py_script.cpp

all: ipc

ipc: $(SOURCES)
	$(CC) $(CPPFLAGS) $(SOURCES) $(LDFLAGS) -o $@

#run: tut
	./ipc

clean:
	rm -f *.o ipc
