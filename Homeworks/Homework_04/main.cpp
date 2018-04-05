#include <iostream>
#include "colors.h"

using namespace std;

int main(int argc, char* argv[]) {
	unsigned char* c = colors[atoi(argv[1])];
	printf("%d %d %d\n", c[0], c[1], c[2]);
	return 0;
}
