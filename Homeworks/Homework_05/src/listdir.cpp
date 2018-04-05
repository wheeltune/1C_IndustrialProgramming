#include "listdir.h"
#include <boost/filesystem.hpp>
#include <boost/range/iterator_range.hpp>

using namespace boost::filesystem;

std::vector<std::string> listDir(const std::string& input_path) {
	path p(input_path);
  
	std::vector<std::string> list_dir;
	directory_iterator end_itr;

    // cycle through the directory
    for (directory_iterator itr(p); itr != end_itr; ++itr) {
        std::string current_file = itr->path().string();
		list_dir.push_back(current_file);
    }
  
	return list_dir;
}
