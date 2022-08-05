#!/usr/bin/env python3
from pathlib import Path
import sys, os

makexample = """
CMAKE_GEN_PATH=generate_cmake.py
PICO_MOUNTPATH=/mnt/pico
MAKEOPTS=-j9

compile: build/$(project_name).uf2 

upload: build/$(PROJECT_NAME).uf2 $(PICO_MOUNTPATH)/INDEX.HTM
	cp build/$(PROJECT_NAME).uf2 $(PICO_MOUNTPATH)

build/$(project_name).uf2: build 
	cd build && make $(MAKEOPTS) && cd ..

build: CMakeLists.txt
	rmdir build ; mkdir build ; cd build && cmake .. && cd ..

CMakeLists.txt:
	python3 $(CMAKE_GEN_PATH)
"""

generate_cmake_example = """
import sys

part1 = ""
part1 += "# Set minimum required version of CMake\\n"
part1 += "cmake_minimum_required(VERSION 3.12)\\n\\n"

part1 += "#include build functions from Pico SDK\\n"
part1 += "include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)\\n"


part2 = ""
part2 += "set(CMAKE_C_STANDARD 11)\\n"
part2 += "set(CMAKE_CXX_STANDARD 17)\\n\\n"

part2 += "# Creates a pico-sdk subdirectory in our project for the libraries\\n"
part2 += "pico_sdk_init()\\n\\n"

part2 += "# point out the CMake, where to find the executable source file\\n"
part2 += "add_executable(${PROJECT_NAME}\\n"
part2 += "        main.c\\n"
part2 += ")\\n\\n"

part2 += "# create map/bin/hex/uf2 files.\\n"
part2 += "pico_add_extra_outputs(${PROJECT_NAME})\\n"

part2 += "# Pull in our pico_stdlib which pulls in commonly used features (gpio, timer-delay etc)\\n"
part2 += "target_link_libraries(${PROJECT_NAME}\\n"
part2 += "            pico_stdlib\\n"
part2 += ")\\n"

cmake_str = part1 + f"\\nproject({project_name} C CXX ASM)\\n" + part2

# write to CMakeLists.txt
try:
	with open("CMakeLists.txt", "w+") as file:
		file.write(cmake_str)
except:
	print("Cannot write to CMakeLists.txt")
	exit()
print("Generated CMakeLists.txt.")

"""

main_example = """\
#include "pico/stdlib.h"

int main() {
	
}
"""

def usage():
	return f"Usage: <{sys.argv[0]}> project_path/project_name"


# (project_folder: Path, project_name: str)
def parse():
	if len(sys.argv) != 2: return usage()

	project_folder, project_name = None, None
	if "/" in sys.argv[1]:
		last_slash = [i for i, val in enumerate(sys.argv[1]) if val == "/"][-1]
		project_folder = Path(sys.argv[1][:last_slash+1])
		project_name = sys.argv[1][last_slash+1:]
	else:
		project_folder = Path("")
		project_name = sys.argv[1]

	# "generate_make.py tests/" gibi kullanıldığında patlamayalım diye
	if project_name == "": return usage()
	return project_folder, project_name


def write_makefile(project_folder, project_name):
	makestr = f"PROJECT_NAME={project_name}\n" + makexample

	try:
		# Eğer klasör yoksa oluştur
		if not project_folder.exists():
			project_folder.mkdir(parents=True, exist_ok=True)
	except:
		return 0, "Cannot create project folders."

	try:
		# Dosyaya yaz
		with project_folder.joinpath("Makefile").open(mode="w+") as file:
			file.write(makestr)
	except:
		return 0, "Cannot write to Makefile."
	return 1, f"[{sys.argv[0]}] Generated Makefile."


def generate_generate_cmake(project_folder, project_name):
	_generate_cmake_example = f"project_name = \"{project_name}\"\n\n" + generate_cmake_example
	try:
		with project_folder.joinpath("generate_cmake.py").open(mode="w+") as file:
			file.write(_generate_cmake_example)
	except:
		return "Cannot generate generate_cmake.py."
	return True 


def main():
	if type(parse_rv := parse()) == str: return parse_rv
	new_folder = not parse_rv[0].exists()
	if (write_rv := write_makefile(*parse_rv))[0] == 0: return write_rv[1]
	print(write_rv[1])
	if type(generate_rv := generate_generate_cmake(*parse_rv)) == str: return generate_rv
	

	if new_folder:
		print(f"[{sys.argv[0]}] Generating new project.")
		os.chdir(parse_rv[0])
		with open("main.c", "w+") as file:
			file.write(main_example)
		os.system("make build")


if __name__ == "__main__":
	main()
