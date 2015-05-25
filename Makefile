all:
	g++ a.cc -o run -O2 -Wall -lm -std=c++11
clean:
	rm run
