main: main.o rsa.o
	gcc -g -lgmp -o main main.o rsa.o

main.o: main.c
	gcc -g -c main.c

rsa.o: rsa.c
	gcc -g -c rsa.c

clean:
	rm -rf main *.o
