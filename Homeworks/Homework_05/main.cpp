#include <iostream>
#include <vector>
#include <listdir.h>


int main(int argc, char* argv[]) {
	std::string path = ".";
	auto result = listDir(path);
  
	for (auto output: result) {
		std::cout << output << std::endl;  
	}
	return 0;
}
