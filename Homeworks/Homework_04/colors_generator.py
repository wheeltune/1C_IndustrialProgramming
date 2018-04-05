import sys

def red(gray):
	return int(255 * (gray / 255.0) ** (1.0 / 2.0))

def green(gray):
	return int(255 * (gray / 255.0) ** (1.0 / 3.0))

def blue(gray):
	return int(255 * (gray / 255.0) ** (1.0 / 4.0))


if __name__ == '__main__':
	output_file = sys.argv[1]
	with open(output_file, 'w') as colors_file:
		colors_file.write("unsigned char colors[256][3] = {")
		for i, gray in enumerate(range(256)):
			colors_file.write("{" + "{}, {}, {}".format(red(gray), green(gray), blue(gray)) + "}")
			if i < 255:
				colors_file.write(", ")

		colors_file.write("};")
